package com.example.namazvakti.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.namazvakti.data.DailyQuote
import com.example.namazvakti.data.NamazRepository
import com.example.namazvakti.data.PrayerData
import com.example.namazvakti.data.Province
import com.example.namazvakti.data.RemainingTimeInfo
import com.example.namazvakti.data.getDailyQuote
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import java.util.Calendar

data class NamazUiState(
    val selectedProvince: Province,
    val prayerData: PrayerData? = null,
    val remainingInfo: RemainingTimeInfo? = null,
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val quote: DailyQuote = getDailyQuote(),
    val isProvincePickerOpen: Boolean = false
)

class NamazViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = NamazRepository(application.applicationContext)

    private val _uiState = MutableStateFlow(
        NamazUiState(selectedProvince = repository.getSavedProvince())
    )
    val uiState: StateFlow<NamazUiState> = _uiState.asStateFlow()

    init {
        loadTimings()
        startTimerLoop()
    }

    fun selectProvince(province: Province) {
        repository.saveSelectedProvince(province)
        _uiState.update { it.copy(selectedProvince = province, isProvincePickerOpen = false) }
        loadTimings(force = false)
    }

    fun openProvincePicker() {
        _uiState.update { it.copy(isProvincePickerOpen = true) }
    }

    fun closeProvincePicker() {
        _uiState.update { it.copy(isProvincePickerOpen = false) }
    }

    fun refresh() {
        loadTimings(force = true)
    }

    private fun loadTimings(force: Boolean = false) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }
            try {
                val province = _uiState.value.selectedProvince
                val data = repository.getPrayerTimes(province, forceRefresh = force)
                val remaining = repository.calculateRemaining(data)
                _uiState.update {
                    it.copy(
                        prayerData = data,
                        remainingInfo = remaining,
                        isLoading = false,
                        errorMessage = null,
                        quote = getDailyQuote()
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        isLoading = false,
                        errorMessage = "Vakitler yüklenemedi: ${e.message}"
                    )
                }
            }
        }
    }

    private fun startTimerLoop() {
        viewModelScope.launch {
            while (isActive) {
                delay(1000)
                val currentData = _uiState.value.prayerData
                if (currentData != null) {
                    val remaining = repository.calculateRemaining(currentData, Calendar.getInstance())
                    _uiState.update { it.copy(remainingInfo = remaining) }
                }
            }
        }
    }
}
