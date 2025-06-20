import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';

export interface UserProfile {
  department?: number | null;
  department_id?: number | null;
  position: string;
  phone_number: string;
  is_department_manager: boolean;
}

export interface Department {
  id: number;
  name: string;
  ticket_count: number;
  description: string;
  contact_email: string;
  identification: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  is_staff: boolean;
  is_superuser: boolean;
  profile: UserProfile | null;
  department?: Department;
}

interface LoginData {
  username: string;
  password: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => {
    const storedToken = localStorage.getItem('access_token');
    console.log('Odczytywanie tokenu z localStorage:', storedToken ? `${storedToken.substring(0, 30)}...` : 'BRAK');

    return {
      user: null as User | null,
      token: storedToken,
      isAuthenticated: !!storedToken,
      isLoading: false,
      error: null as string | null,
    };
  },

  actions: {
    async login(loginData: LoginData) {
      this.isLoading = true;
      this.error = null;

      try {
        console.log('Próba logowania...');
        const response = await axios.post(
          'http://localhost:8000/api/auth/login/',
          loginData
        );

        console.log('Odpowiedź logowania:', response.data);
        console.log('Klucze w response.data:', Object.keys(response.data));

        const token = response.data.access || response.data.access_token || response.data.token;

        if (!token) {
          console.error('Brak tokenu w odpowiedzi:', response.data);
          this.error = 'Brak tokenu w odpowiedzi serwera';
          return false;
        }

        this.token = token;
        this.isAuthenticated = true;

        localStorage.setItem('access_token', token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        console.log('Token ustawiony w axios headers');

        await this.fetchUserProfile();

        router.push('/dashboard');
        return true;

      } catch (error: any) {
        this.error =
          error.response?.data?.error ||
          error.response?.data?.detail ||
          'Błąd logowania';

        console.error('Błąd logowania:', error);
        return false;

      } finally {
        this.isLoading = false;
      }
    },

    async fetchUserProfile() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) return;

        const response = await axios.get('http://localhost:8000/api/users/me/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        this.user = response.data;
        console.log('Pobrane dane użytkownika:', this.user);
      } catch (error) {
        const token = localStorage.getItem('access_token');
        if (!token) return;

        console.error('Błąd pobierania profilu użytkownika:', error);
        
        try {
          const response = await axios.get('http://localhost:8000/api/auth/user/', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });
          
          this.user = response.data;
          console.log('Dane użytkownika pobrane z alternatywnego endpointu');
        } catch (fallbackError) {
          console.error('Błąd alternatywnej metody pobierania użytkownika:', fallbackError);
        }
      }
    },

    async initializeAuth() {
      const token = localStorage.getItem('access_token');
      console.log('Inicjalizacja auth, token z localStorage:', token ? `${token.substring(0, 30)}...` : 'BRAK');

      if (token && token !== 'undefined' && token !== 'null') {
        this.token = token;
        this.isAuthenticated = true;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        console.log('Token zainicjalizowany w axios');
        
        await this.fetchUserProfile();
        
        await this.initializeOtherStores();
      } else {
        console.log('Brak ważnego tokenu - wylogowywanie...');
        this.logout();
      }
    },

    async initializeOtherStores() {
      try {
        const { useTicketStore } = await import('./ticketStore');
        const ticketStore = useTicketStore();
        await ticketStore.initializeStore();
      } catch (error) {
        console.log('Błąd inicjalizacji innych store:', error);
      }
    },

    logout() {
      console.log('Wylogowywanie...');
      
      this.resetOtherStores();
      
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('access_token');
      delete axios.defaults.headers.common['Authorization'];
      router.push('/login');
    },

    async resetOtherStores() {
      try {
        const { useTicketStore } = await import('./ticketStore');
        const ticketStore = useTicketStore();
        ticketStore.resetStore();
      } catch (error) {
        console.log('Błąd resetowania store:', error);
      }
    }
  }
});