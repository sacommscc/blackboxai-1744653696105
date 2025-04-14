import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Async thunks
export const fetchVendors = createAsyncThunk(
  'vendors/fetchVendors',
  async (_, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/vendors/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const addVendor = createAsyncThunk(
  'vendors/addVendor',
  async (vendorData, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/vendors/`, vendorData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const updateVendor = createAsyncThunk(
  'vendors/updateVendor',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(`${API_URL}/vendors/${id}/`, data, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const deleteVendor = createAsyncThunk(
  'vendors/deleteVendor',
  async (id, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/vendors/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return id;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchVendorProducts = createAsyncThunk(
  'vendors/fetchVendorProducts',
  async (vendorId, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/vendors/${vendorId}/products/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return { vendorId, products: response.data };
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const addVendorProduct = createAsyncThunk(
  'vendors/addVendorProduct',
  async ({ vendorId, productData }, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/vendors/${vendorId}/products/`,
        productData,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  vendors: [],
  vendorProducts: {},
  isLoading: false,
  error: null,
  selectedVendor: null,
};

const vendorSlice = createSlice({
  name: 'vendors',
  initialState,
  reducers: {
    setSelectedVendor: (state, action) => {
      state.selectedVendor = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Vendors
      .addCase(fetchVendors.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchVendors.fulfilled, (state, action) => {
        state.isLoading = false;
        state.vendors = action.payload;
      })
      .addCase(fetchVendors.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to fetch vendors';
      })
      // Add Vendor
      .addCase(addVendor.fulfilled, (state, action) => {
        state.vendors.push(action.payload);
      })
      // Update Vendor
      .addCase(updateVendor.fulfilled, (state, action) => {
        const index = state.vendors.findIndex((v) => v.id === action.payload.id);
        if (index !== -1) {
          state.vendors[index] = action.payload;
        }
      })
      // Delete Vendor
      .addCase(deleteVendor.fulfilled, (state, action) => {
        state.vendors = state.vendors.filter((v) => v.id !== action.payload);
      })
      // Fetch Vendor Products
      .addCase(fetchVendorProducts.fulfilled, (state, action) => {
        state.vendorProducts[action.payload.vendorId] = action.payload.products;
      })
      // Add Vendor Product
      .addCase(addVendorProduct.fulfilled, (state, action) => {
        const vendorId = action.payload.vendor;
        if (!state.vendorProducts[vendorId]) {
          state.vendorProducts[vendorId] = [];
        }
        state.vendorProducts[vendorId].push(action.payload);
      });
  },
});

export const { setSelectedVendor, clearError } = vendorSlice.actions;

export default vendorSlice.reducer;

// Selectors
export const selectVendors = (state) => state.vendors.vendors;
export const selectVendorProducts = (state) => state.vendors.vendorProducts;
export const selectSelectedVendor = (state) => state.vendors.selectedVendor;
export const selectIsLoading = (state) => state.vendors.isLoading;
export const selectError = (state) => state.vendors.error;
