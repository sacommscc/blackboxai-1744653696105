import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Async thunks
export const fetchLabourTypes = createAsyncThunk(
  'labour/fetchLabourTypes',
  async (_, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/labour/types/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchLabourers = createAsyncThunk(
  'labour/fetchLabourers',
  async (_, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/labour/labourers/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const addLabourer = createAsyncThunk(
  'labour/addLabourer',
  async (labourerData, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/labour/labourers/`, labourerData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const updateLabourer = createAsyncThunk(
  'labour/updateLabourer',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(`${API_URL}/labour/labourers/${id}/`, data, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const addWorkLog = createAsyncThunk(
  'labour/addWorkLog',
  async (workLogData, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/labour/work-logs/`, workLogData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchLabourerWorkLogs = createAsyncThunk(
  'labour/fetchLabourerWorkLogs',
  async (labourerId, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/labour/labourers/${labourerId}/work-logs/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return { labourerId, workLogs: response.data };
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const addLabourPayment = createAsyncThunk(
  'labour/addLabourPayment',
  async (paymentData, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/labour/payments/`, paymentData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  labourTypes: [],
  labourers: [],
  workLogs: {},
  payments: [],
  isLoading: false,
  error: null,
  selectedLabourer: null,
};

const labourSlice = createSlice({
  name: 'labour',
  initialState,
  reducers: {
    setSelectedLabourer: (state, action) => {
      state.selectedLabourer = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Labour Types
      .addCase(fetchLabourTypes.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchLabourTypes.fulfilled, (state, action) => {
        state.isLoading = false;
        state.labourTypes = action.payload;
      })
      .addCase(fetchLabourTypes.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch labour types';
      })
      // Fetch Labourers
      .addCase(fetchLabourers.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchLabourers.fulfilled, (state, action) => {
        state.isLoading = false;
        state.labourers = action.payload;
      })
      .addCase(fetchLabourers.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch labourers';
      })
      // Add Labourer
      .addCase(addLabourer.fulfilled, (state, action) => {
        state.labourers.push(action.payload);
      })
      // Update Labourer
      .addCase(updateLabourer.fulfilled, (state, action) => {
        const index = state.labourers.findIndex((l) => l.id === action.payload.id);
        if (index !== -1) {
          state.labourers[index] = action.payload;
        }
      })
      // Add Work Log
      .addCase(addWorkLog.fulfilled, (state, action) => {
        const labourerId = action.payload.labourer;
        if (!state.workLogs[labourerId]) {
          state.workLogs[labourerId] = [];
        }
        state.workLogs[labourerId].push(action.payload);
      })
      // Fetch Labourer Work Logs
      .addCase(fetchLabourerWorkLogs.fulfilled, (state, action) => {
        state.workLogs[action.payload.labourerId] = action.payload.workLogs;
      })
      // Add Labour Payment
      .addCase(addLabourPayment.fulfilled, (state, action) => {
        state.payments.push(action.payload);
      });
  },
});

export const { setSelectedLabourer, clearError } = labourSlice.actions;

export default labourSlice.reducer;

// Selectors
export const selectLabourTypes = (state) => state.labour.labourTypes;
export const selectLabourers = (state) => state.labour.labourers;
export const selectWorkLogs = (state) => state.labour.workLogs;
export const selectPayments = (state) => state.labour.payments;
export const selectSelectedLabourer = (state) => state.labour.selectedLabourer;
export const selectIsLoading = (state) => state.labour.isLoading;
export const selectError = (state) => state.labour.error;
