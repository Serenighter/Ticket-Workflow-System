import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from './authStore'

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  is_staff: boolean;
  is_superuser: boolean;
  profile: null | any;
  department?: Department;
}

interface Department {
  id: number;
  name: string;
  ticket_count: number;
  description: string;
  contact_email: string;
  identification: string;
  updated_at: string;
}

export interface Ticket {
  id: number;
  created_by: User;
  assigned: User | null;
  of_department: Department | null;
  status_display: string;
  priority_display: string;
  category_display: string;
  title: string;
  description: string;
  category: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
  due: string | null;
  closed_at: string | null;
}

export interface TicketCreate {
  title: string;
  description: string;
  category: string;
  priority: string;
  due?: string | null;
  assigned?: number | null;
  of_department?: number | null;
}

export const useTicketStore = defineStore('ticket', () => {
  const tickets = ref<Ticket[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const initialized = ref(false)

  const getTickets = async () => {
    isLoading.value = true
    error.value = null

    try {
      const token = localStorage.getItem('access_token')

      if (!token) {
        error.value = 'Brak autoryzacji - zaloguj się ponownie'
        return
      }

      const response = await axios.get('http://localhost:8000/api/tickets/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      tickets.value = response.data.results || response.data
      initialized.value = true
      console.log('Tickety pobrane:', tickets.value.length)

    } catch (err: any) {
      console.error('Błąd pobierania ticketów:', err)
      if (err.response?.status === 401) {
        error.value = 'Sesja wygasła - zaloguj się ponownie'
        const authStore = useAuthStore()
        authStore.logout()
      } else if (err.response?.status === 403) {
        error.value = 'Brak uprawnień do przeglądania ticketów'
      } else {
        error.value = 'Błąd pobierania zgłoszeń'
      }
    } finally {
      isLoading.value = false
    }
  }

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) return null

      const response = await axios.get('http://localhost:8000/api/auth/user/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      return response.data
    } catch (error) {
      console.error('Błąd pobierania danych użytkownika:', error)
      return null
    }
  }

  const initializeStore = async () => {
    if (!initialized.value) {
      const authStore = useAuthStore()
      if (authStore.isAuthenticated) {
        await getTickets()
      }
    }
  }

  const resetStore = () => {
    tickets.value = []
    initialized.value = false
    error.value = null
    isLoading.value = false
  }

  const createTicket = async (ticketData: TicketCreate) => {
  isLoading.value = true;
  error.value = null;

  try {
    const token = localStorage.getItem('access_token');
    const authStore = useAuthStore();

    if (!token) {
      error.value = 'Brak autoryzacji - zaloguj się ponownie';
      return false;
    }

    console.log('Auth store user:', authStore.user);

    let departmentId = authStore.user?.department?.id || 
                      authStore.user?.department || 
                      ticketData.of_department;

    if (!departmentId) {
      console.log('Brak działu w authStore, pobieranie danych użytkownika...');
      const userData = await fetchUserData();
      console.log('Pobrane dane użytkownika:', userData);
      
      if (userData?.department?.id) {
        departmentId = userData.department.id;
        authStore.user = userData;
      } else if (userData?.department) {
        departmentId = userData.department;
      }
    }

    let finalDepartmentId: number | null = null;
    
    if (departmentId) {
      finalDepartmentId = typeof departmentId === 'string' ? parseInt(departmentId, 10) : Number(departmentId);
    }

    if (!finalDepartmentId || isNaN(finalDepartmentId) || finalDepartmentId <= 0) {
      error.value = 'Nie znaleziono działu użytkownika. Skontaktuj się z administratorem.';
      console.error('Brak departmentId po wszystkich próbach lub nieprawidłowy format');
      return false;
    }

    console.log('Używany departmentId (po konwersji):', finalDepartmentId, typeof finalDepartmentId);

    const categoryMapping: Record<string, string> = {
      'Problem ze sprzętem': 'HARDWARE_FAILURE',
      'Problem z oprogramowaniem': 'SOFTWARE_FAILURE',
      'Zapotrzebowanie na sprzęt': 'DEVICE_NEEDS',
    };

    const priorityMapping: Record<string, string> = {
      'Niski': 'LOW',
      'Średni': 'MEDIUM',
      'Wysoki': 'HIGH',
      'Najwyższy': 'URGENT'
    };

    const payload = {
      title: ticketData.title,
      description: ticketData.description,
      category: categoryMapping[ticketData.category] || ticketData.category,
      priority: priorityMapping[ticketData.priority] || ticketData.priority,
      due: ticketData.due ? new Date(ticketData.due).toISOString() : null,
      assigned: ticketData.assigned || null,
      of_department: finalDepartmentId 
    };

    console.log("=== POPRAWNY PAYLOAD ===");
    console.log("Wysyłane dane (finalne):", payload);
    console.log("of_department:", payload.of_department);
    console.log("Typ of_department:", typeof payload.of_department);
    console.log("Czy of_department jest null?", payload.of_department === null);
    console.log("Czy of_department jest undefined?", payload.of_department === undefined);
    console.log("JSON.stringify payload:", JSON.stringify(payload, null, 2));
    console.log("=== KONIEC DEBUG PAYLOAD ===");

    const requiredFields = ['title', 'description', 'category', 'priority', 'of_department'];
    const missingFields = requiredFields.filter(field => !payload[field as keyof typeof payload]);
    
    if (missingFields.length > 0) {
      error.value = `Brakujące wymagane pola: ${missingFields.join(', ')}`;
      console.error('Brakujące pola:', missingFields);
      return false;
    }

    const response = await axios.post('http://localhost:8000/api/tickets/', payload, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    console.log('Ticket utworzony:', response.data);
    
    tickets.value.unshift(response.data);
    
    return response.data;

  } catch (err: any) {
    console.error('Błąd tworzenia ticketu:', err);
    
    if (err.response) {
      console.error('Odpowiedź serwera:', err.response.data);
      console.error('Status:', err.response.status);
      
      if (err.response.status === 401) {
        error.value = 'Sesja wygasła - zaloguj się ponownie';
        const authStore = useAuthStore();
        authStore.logout();
      } else if (err.response.status === 403) {
        error.value = 'Brak uprawnień do tworzenia zgłoszeń';
      } else if (err.response.status === 400) {
        const errors = Object.entries(err.response.data)
          .map(([key, value]) => {
            if (Array.isArray(value)) {
              return `${key}: ${value.join(', ')}`;
            }
            return `${key}: ${value}`;
          })
          .join('\n');
        error.value = `Błędy walidacji:\n${errors}`;
      } else if (err.response.status === 500) {
        if (typeof err.response.data === 'string' && err.response.data.includes('NOT NULL constraint failed')) {
          error.value = 'Błąd bazy danych: brakuje wymaganego pola działu. Sprawdź swoje uprawnienia.';
        } else {
          error.value = 'Błąd wewnętrzny serwera';
        }
      } else {
        error.value = err.response.data.detail || 'Nieznany błąd serwera';
      }
    } else if (err.request) {
      error.value = 'Brak odpowiedzi serwera - sprawdź połączenie';
    } else {
      error.value = 'Błąd podczas konfiguracji żądania';
    }
    
    return false;
  } finally {
    isLoading.value = false;
  }
}

 const deleteTicket = async (ticketId: number) => {
    isLoading.value = true;
    error.value = null;

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        error.value = 'Brak autoryzacji - zaloguj się ponownie';
        return false;
      }

      await axios.delete(`http://localhost:8000/api/tickets/${ticketId}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      tickets.value = tickets.value.filter(ticket => ticket.id !== ticketId);
      
      return true;
    } catch (err: any) {
      console.error('Błąd usuwania ticketu:', err);
      
      if (err.response?.status === 401) {
        error.value = 'Sesja wygasła - zaloguj się ponownie';
        const authStore = useAuthStore();
        authStore.logout();
      } else if (err.response?.status === 403) {
        error.value = 'Brak uprawnień do usunięcia zgłoszenia';
      } else if (err.response?.status === 404) {
        error.value = 'Zgłoszenie nie istnieje';
      } else {
        error.value = 'Błąd podczas usuwania zgłoszenia';
      }
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    tickets,
    isLoading,
    error,
    initialized,
    getTickets,
    initializeStore,
    resetStore,
    createTicket,
    fetchUserData,
    deleteTicket
  }
})