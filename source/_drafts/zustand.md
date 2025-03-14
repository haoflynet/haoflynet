## 基础使用

### 定义Store

```ts
import { create } from 'zustand';
import { createJSONStorage, persist, StateStorage } from 'zustand/middleware';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import {LoginResponse} from "@/types/LoginResponse";

interface UserState {
  isLoggedIn: boolean;
  username: string;
  accessToken?: string;
  refreshToken?: string;
  setLogin: (loginResponse: LoginResponse) => void;
  logout: () => void;
}

const SecureStorage: StateStorage = {
  getItem: async (name: string): Promise<string | null> => {
    if (Platform.OS === 'web') {
      return localStorage.getItem(name);
    } else {
      return (await SecureStore.getItemAsync(name)) || null;
    }
  },
  setItem: async (name: string, value: string): Promise<void> => {
    if (Platform.OS === 'web') {
      localStorage.setItem(name, value);
    } else {
      await SecureStore.setItemAsync(name, value);
    }
  },
  removeItem: async (name: string): Promise<void> => {
    if (Platform.OS === 'web') {
      localStorage.removeItem(name);
    } else {
      await SecureStore.deleteItemAsync(name);
    }
  },
};

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      isLoggedIn: false,
      username: '',
      setLogin: (loginResponse: LoginResponse) => set({
        isLoggedIn: true,
        username: loginResponse.username,
        accessToken: loginResponse.access_token,
        refreshToken: loginResponse.refresh_token,
      }),
      logout: () => set({
        isLoggedIn: false,
        username: '',
        accessToken: undefined,
        refreshToken: undefined,
      }),
    }),
    {
      name: 'user-storage',
      storage: createJSONStorage(() => SecureStorage),
    },
  ),
);
```

### 使用Store

```ts
const accesstoken = useUserStore(state => state.accessToken);

// 在非函数组件中同样可以这样获取
const accessToken = useUserStore.getState().accessToken;
```

