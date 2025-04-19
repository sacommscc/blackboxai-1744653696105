import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Async thunks
// Hardcoded admin credentials
const ADMIN_EMAIL = 'admin@example.com';
const ADMIN_PASSWORD = 'admin123';
const MOCK_TOKEN = 'mock-jwt-token';

export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }, { rejectWithValue }) => {
    // Comment out actual API call and use hardcoded check
    // try {
    //   const response = await axios.post(`${API_URL}/auth/login/`, {
    //     email,
    //     password,
    //   });
    //   localStorage.setItem('token', response.data.token);
    //   return response.data;
    // } catch (error) {
    //   return rejectWithValue(error.response.data);
    // }

    // Check against hardcoded credentials
    if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
      const mockResponse = {
        token: MOCK_TOKEN,
        user: {
          id: 1,
          email: ADMIN_EMAIL,
          role: 'admin',
          first_name: 'Admin',
          last_name: 'User'
        }
      };
      localStorage.setItem('token', MOCK_TOKEN);
      return mockResponse;
    }
    return rejectWithValue({ message: 'Invalid credentials' });
  }
);

export const logout = createAsyncThunk('auth/logout', async () => {
  localStorage.removeItem('token');
  // Call backend logout endpoint with POST to clear session
  try {
    await fetch('http://localhost:8000/logout/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Logout error:', error);
  }
  return null;
});

export const getCurrentUser = createAsyncThunk(
  'auth/getCurrentUser',
  async (_, { rejectWithValue }) => {
    // Comment out actual API call and use hardcoded response
    // try {
    //   const token = localStorage.getItem('token');
    //   if (!token) return null;

    //   const response = await axios.get(`${API_URL}/auth/user/`, {
    //     headers: { Authorization: `Bearer ${token}` },
    //   });
    //   return response.data;
    // } catch (error) {
    //   return rejectWithValue(error.response.data);
    // }

    const token = localStorage.getItem('token');
    if (token === MOCK_TOKEN) {
      return {
        id: 1,
        email: ADMIN_EMAIL,
        role: 'admin',
        first_name: 'Admin',
        last_name: 'User'
      };
    }
    return null;
  }
);

const initialState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Login failed';
      })
      // Logout
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
        state.token = null;
        state.isAuthenticated = false;
        state.isLoading = false;
      })
      // Get Current User
      .addCase(getCurrentUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = !!action.payload;
        state.user = action.payload;
      })
      .addCase(getCurrentUser.rejected, (state) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      });
  },
});

export const { clearError } = authSlice.actions;

export default authSlice.reducer;

// Selectors
export const selectAuth = (state) => state.auth;
export const selectUser = (state) => state.auth.user;
export const selectIsAuthenticated = (state) => state.auth.isAuthenticated;
export const selectIsLoading = (state) => state.auth.isLoading;
export const selectError = (state) => state.auth.error;
