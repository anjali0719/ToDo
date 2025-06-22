import { Routes } from "@angular/router";

export const userRoutes: Routes = [
    {
        path: 'sign-in',
        loadComponent: () => import('./sign-in/sign-in.component').then(m => m.SignInComponent),
        data: {
            title: 'Sign In'
        }
    },
    {
        path: 'sign-up',
        loadComponent: () => import('./sign-up/sign-up.component').then(m => m.SignUpComponent),
        data: {
            title: 'Sign Up'
        }
    },
    {
        path: 'change-password',
        loadComponent: () => import('./passwords/change-password/change-password.component').then(m => m.ChangePasswordComponent),
        data: {
            title: 'Change Password'
        }
    }
];
