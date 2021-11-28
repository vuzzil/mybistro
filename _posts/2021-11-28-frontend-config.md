---
layout: single
title:  "MyBistro--FrontEnd Configuration"
date:   2021-11-28 21:00:00 +0800
categories: doc
toc: true
toc_label: "Contents"
---

## 前端是以React 開發的App
### 啟始一個新的react專案
可以使用npm 內建的指令:npx，  
(是一種CLI,要在命令列執行)  
新增工作目錄:ex:D:\working\react-my-app
``` terminal
$>npx create-react-app my-app
```
就可以創建React app的初使開發環境

快速安裝所有需要的套件:  
update package.json
```
"dependencies": {
    "@emotion/react": "^11.4.1",
    "@emotion/styled": "^11.3.0",
    "@mui/icons-material": "^5.0.3",
    "@mui/material": "^5.0.3",
    "@testing-library/jest-dom": "^5.14.1",
    "@testing-library/react": "^11.2.7",
    "@testing-library/user-event": "^12.8.3",
    "axios": "^0.24.0",
    "formik": "^2.2.9",
    "history": "^5.0.1",
    "node-sass": "^6.0.1",
    "react": "^17.0.2",
    "react-device-detect": "^2.0.1",
    "react-dom": "^17.0.2",
    "react-perfect-scrollbar": "^1.5.8",
    "react-redux": "^7.2.5",
    "react-router-dom": "^6.0.0-beta.6",
    "react-scripts": "4.0.3",
    "web-vitals": "^1.1.2",
    "yup": "^0.32.11"
  },
```
然後執行:
``` terminal
$>npm install
```

### 整合Material UI(MUI)
為何採用[MUI](https://mui.com/getting-started/usage/){:target="_blank"}，因為最多人用，Components也滿夠用，也算漂亮。  
#### 安裝需要的套件:
``` terminal
$>npm install @mui/material @emotion/react @emotion/styled   //For material UI
$>npm install @mui/icons-material             //For material UI's icons
```
注意MUI V5.0以後，style的語法和V4以前改滿多的，makeStyles已經不用了
``` js
const useStyles = makeStyles((theme) => ({
    ...
  }
}));
```
所以想要參考MUI template的範例，都要改成如下的新語法。
``` js
const Nav = styled('nav')(({ theme }) => ({
    [theme.breakpoints.up('md')]: {
        width: drawerWidth,
        flexShrink: 0
    },
}));
```
#### Theme

+   新增Theme     
ex:/src/themes/botanical.js  

``` js
import { createTheme } from '@mui/material/styles';

//botanical theme
const botanical = createTheme({
    palette: {
        //mode: 'dark',
        primary: {
            main: '#6e8c75',
            light:'#ebfff6',
            dark: '#415245',            
        },
        secondary: {
            main: '#787d7a',
        },
        warning: {
            main: '#d6922d',
        },
        info: {
            main: '#37607f',
        },
        success: {
            main: '#4b5c6b',
            light: '#9bb3c7',
            dark: '#39444d',
        },
        background: {
            paper: '#ced9d9',
            default: '#f2ffff',
        },
    },
});

export default botanical;
```

+   新增ThemeProvider  
ex: /src/themes/CustomThemeProvider.js  

``` js
import React, { createContext, useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { useSelector } from 'react-redux';


//predefined themes
import LightTheme from './LightTheme';
import botanical from './botanical';

export const CustomThemeContext = createContext({
	currentTheme: 'light',
	setTheme: null
});

//mui default theme 
const mui = createTheme();
const dark = createTheme({
	palette: {
		mode: 'dark',
	},
});

const CustomThemeProvider = props => {
	const { children } = props;

	const customization = useSelector((state) => state.customization);
	const light = LightTheme(customization);
	
	const themes = {
		light,
		mui,
		botanical,
		dark,
	}

	const getTheme = (theme) => {
		return themes[theme];
	}

	// Get current theme from localStorage
	let currentTheme = localStorage.getItem('appTheme') ?? 'light';
	currentTheme = (currentTheme === "null") ? 'light' : currentTheme;

	// State to hold selected theme
	const [themeName, _setThemeName] = useState(currentTheme);

	// Retrieve theme object by theme name
	const theme = getTheme(themeName);
	console.log("themeName=" + themeName + ",theme=" + theme);

	// Wrap _setThemeName to store new theme names in localStorage
	const setThemeName = name => {
		localStorage.setItem('appTheme', name);
		_setThemeName(name);
	};

	const contextValue = {
		currentTheme: themeName,
		setTheme: setThemeName
	};

	return (
		<CustomThemeContext.Provider value={contextValue}>
			<ThemeProvider theme={theme}>{children}</ThemeProvider>
		</CustomThemeContext.Provider>
	);
};

export default CustomThemeProvider;
```

+   修改根目錄下的:App.js,     
add &lt;StyledEngineProvider&gt;,&lt;CustomThemeProvider&gt;

``` jsx
import { StyledEngineProvider, CssBaseline } from '@mui/material';
import CustomThemeProvider from 'themes/CustomThemeProvider';
...
function App() {
  ...
  return (
    <StyledEngineProvider injectFirst>
      <CustomThemeProvider>
        <CssBaseline />
        <Routes isLoggedIn={isLoggedIn} />
      </CustomThemeProvider>
    </StyledEngineProvider>
  );
);
```

### 整合React router
React App屬於SinglePageApp(SPA)，所有頁面其實都是利用JavaScript動態繪製(Render)出來的，
但要模擬像是一般網頁的操作，就要利用router在網址上產生URL，讓人有一種頁面切換的感覺。  
頁面的Component，及所套用的Layout也可以定義在這裡。
#### 安裝需要的套件:
``` terminal
$>npm install react-router-dom
```
#### 整合方法:
修改根目錄下的:index.js,add &lt;BrowserRouter&gt;
``` jsx
ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
);
```

修改根目錄下的:App.js,add &lt;Routes&gt;
``` jsx
// routing
import Routes from './routes';
...
function App() {
  ...
  return (
    <StyledEngineProvider injectFirst>
      <CustomThemeProvider>
        <CssBaseline />
        <Routes isLoggedIn={isLoggedIn} />
      </CustomThemeProvider>
    </StyledEngineProvider>
  );
);
```
新增 /routes/index.js  
使用React Route提供的useRoutes Hook  
將App中會使用到的頁面URL加到此檔。
``` jsx
import { useRoutes } from 'react-router-dom';
...
// ===========================|| MAIN ROUTING ||=========================== //
const AuthRoute = {
    path: '/',
    element: <MiniLayout />,
    children: [
        {
            path: '/',
            element: <Login />
        },
        {
            path: '/login',
            element: <Login />
        },
        ...
    ]
};

const MainRoutes = (isLoggedIn) => {
    return {
        path: '/bistro',
        element: (isLoggedIn) ? <MainLayout /> : <Login />,
        children: [

            {
                path: '/bistro',
                element: <Home />
            },
            {
                path: '/bistro/page1',
                element: <Page1 />
            },
           ...

        ]
    };
}

// ===========================|| ROUTING RENDER ||=========================== //

export default function ThemeRoutes({ isLoggedIn }) {
    return useRoutes([AuthRoute, MainRoutes(isLoggedIn),]);
}
```

### 整合React Redux
#### 安裝需要的套件:
``` terminal
$>npm install react-redux
```
#### 整合方法:
+ 新增/store/actions.js  

``` js  
// action - customization reducer
export const SET_MENU = '@customization/SET_MENU';
export const MENU_OPEN = '@customization/MENU_OPEN';
export const SET_FONT_FAMILY = '@customization/SET_FONT_FAMILY';
export const SET_BORDER_RADIUS = '@customization/SET_BORDER_RADIUS';

// action - auth reducer
export const REGISTER_SUCCESS = "REGISTER_SUCCESS";
export const REGISTER_FAIL = "REGISTER_FAIL";
export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_FAIL = "LOGIN_FAIL";
export const LOGOUT = "LOGOUT";

// action - error Reducer
export const SET_ERROR = "SET_ERROR";
export const HIDE_ERROR = "HIDE_ERROR";
```    
+   新增 Reducer  
ex:/store/authReducer.js   

``` jsx  
...
const user = JSON.parse(localStorage.getItem("user"));

const initialState = user
    ? { isLoggedIn: true, user: { username: user.username, email: user.email, theme: user.theme } }
    : { isLoggedIn: false, user: {} };

const authReducer = (state = initialState, action) => {
    const { type, user } = action;

    switch (type) {
        case REGISTER_SUCCESS:
            return {
                ...state,
                isLoggedIn: false,
            };
        case REGISTER_FAIL:
            return {
                ...state,
                isLoggedIn: false,
            };
        ...
        default:
            return state;
    }
}

export default authReducer;
```  

+   新增 /store/index.js  

``` jsx
import { createStore } from 'redux';
import reducer from './reducer';

// ===========================|| REDUX - MAIN STORE ||=========================== //
const store = createStore(
    reducer
);

export default store;
```

+   修改根目錄下的:index.js,add &lt;Provider&gt;  

``` jsx
import { Provider } from 'react-redux';
// project imports
import store from './store';
...

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
);
```

+   修改根目錄下的:App.js  
使用Redux useSelector Hook,來存取store中的state。  

``` jsx
import { useSelector } from 'react-redux';
...

function App() {
  const isLoggedIn = useSelector((state) => state.auth.isLoggedIn);
  
 ...
}
```

+   store中state的值是在別的Component呼叫dispatch()寫入的。     
ex: state.auth.isLoggedIn 是登入/src/services/auth.service.js寫入的。

``` jsx
...
export const login = (email, password) => {
    return AuthApi.login(email, password).then(
        () => {
            return getLoginUser();
        },
        (error) => {
           ...
            store.dispatch({
                type: LOGIN_FAIL,
            });

            ...
            return Promise.reject(message);
        }
    );
};

export const getLoginUser = () => {
    request("get", "/bistro/user/").then((res) => {

        if (res.data) {
            let user = res.data;
            //console.log("getLoginUser-> user=" + user.username);
            store.dispatch({
                type: LOGIN_SUCCESS,
                user: user,
            });
            return Promise.resolve();
        }

    }).catch(error => {
        ...
        store.dispatch({
            type: LOGIN_FAIL,
        });
        ...
        return Promise.reject(message);
    });
}
```
+   也可以用Redux:useDispatch Hook 呼叫dispatch()。

``` jsx
import { useSelector, useDispatch } from 'react-redux';
...
const dispatch = useDispatch();

const handleLeftDrawerToggle = () => {
        dispatch({ type: SET_MENU, opened: !leftDrawerOpened });
    };
```    

### 呼叫後端API
#### 安裝需要的套件:
``` terminal
$>npm install axios
```
#### 整合方法:

根目錄下新增 .env file
``` 
#For DEV USE.............................................
REACT_APP_API_ROOT_URL=http://127.0.0.1:8000/api

#For PROD USE ...........................................
#REACT_APP_API_ROOT_URL=/api
```
+   新增/src/services/request.js

``` js
import axios from "axios";

const API_ROOT_URL = process.env.REACT_APP_API_ROOT_URL;
// baseURL是Backend API ROOT URL，之後只要填相對路徑

const instance = axios.create({
    baseURL: API_ROOT_URL,
    headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
    },
    timeout: 5000
});
export default function request(method, url, data = null, config) {
    method = method.toLowerCase();
    ...

    switch (method) {
        case "post":
            return instance
                .post(url, data, config)
                .catch(error => {
                    return Promise.reject(new ApiError(error));
                });
        case "get":
            return instance
                .get(url, { params: data }).catch(error => {
                    return Promise.reject(new ApiError(error));
                });
        case "delete":
            return instance
                .delete(url, { params: data })
                .catch(error => {
                    return Promise.reject(new ApiError(error));
                });

        case "put":
            return instance
                .put(url, data)
                .catch(error => {
                    return Promise.reject(new ApiError(error));
                });
        case "patch":
            return instance
                .patch(url, data)
                .catch(error => {
                    return Promise.reject(new ApiError(error));
                });
        default:
            console.log(`未知的 method: ${method}`);
            return Promise.reject(new ApiError(`未知的 method: ${method}`));
    }

```

+   透過request呼叫後端API  
ex:/src/services/bistro.service.js

``` js
import request from "./request";
...
export const getBistroMenus = (params) => {
    return request("get", "/bistro/menus/", params)
        .catch((error) => {
            ...

            return Promise.reject(message);
        });
    ;
};
```

### 整合JWT Anthentication
+   登入時call 後端API:(obtain token)取得token(包含access token和reflesh token),並將token存到localStorage的user物件。        
登出時call 後端API:(logout)將reflesh token加入BlackList使token失效。    
新增/src/services/AuthApi.js    

``` jsx
import axios from "axios";
import request from "./request";

class AuthApi {
  constructor() {
    let API_ROOT_URL = process.env.REACT_APP_API_ROOT_URL;
    this.axioInstance = axios.create({
      baseURL: API_ROOT_URL,
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
      },
      timeout: 5000
    });
  }


  login(email, password) {
    return this.axioInstance.post("/token/obtain/", {
      email,
      password
    })
      .then(response => {
        if (response.data.access) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }

        return response.data;
      });
  }

  logout() {
    let user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      let refresh_token = user.refresh;
      //logout need authentication ,so must use request to do this .....
      return request("post", "/logout/", { refresh_token: refresh_token })
    }
  }

  register(username, email, password) {
    return this.axioInstance.post("/signup/", {
      username,
      email,
      password
    });
  }
}

export default new AuthApi();

```

+   修改/src/services/request.js,    
access token 加入headers['Authorization']部分，才能通過驗證。    
並利用instance.interceptors.response.use自動refresh token。    

``` jsx
...
instance.interceptors.response.use(
    response => response,
    error => {
        const originalRequest = error.config;

        // Prevent infinite loops
        if (error.response && error.response.status === 401 && originalRequest.url === API_ROOT_URL + '/token/refresh/') {
            return Promise.reject(new ApiError(error));
        }

        if (error.response && error.response.status === 401 && error.response.statusText === "Unauthorized") {
            let user = JSON.parse(localStorage.getItem('user'));
            let refresh_token = (user && user.refresh) ? user.refresh : '';


            //Check whether refresh_token is expired
            const tokenParts = JSON.parse(atob(refresh_token.split('.')[1]));
            // exp date in token is expressed in seconds, while now() returns milliseconds:
            const now = Math.ceil(Date.now() / 1000);

            if (tokenParts.exp > now) {
                return instance
                    .post('/token/refresh/', { refresh: refresh_token })
                    .then((response) => {
                        localStorage.setItem("user", JSON.stringify(response.data));

                        instance.defaults.headers['Authorization'] = "JWT " + response.data.access;
                        originalRequest.headers['Authorization'] = "JWT " + response.data.access;

                        return instance(originalRequest);
                    })
                    .catch(err => {
                        console.log("refreshtoken時發生錯誤:");
                        console.log(err)
                        return Promise.reject(new ApiError("refreshtoken 失敗!"));
                    });
            } else {
                console.log("Refresh token is expired", tokenParts.exp, now);
                return Promise.reject(new ApiError("refreshtoken 失敗!,token已逾剘"));
            }
        }
        return Promise.reject(new ApiError(error));
    }
);

export default function request(method, url, data = null, config) {
    method = method.toLowerCase();
    let user = JSON.parse(localStorage.getItem('user'));
    let access_token = (user && user.access) ? user.access : '';
    instance.defaults.headers['Authorization'] = "JWT " + access_token;
    
    ...
}
```