import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/user/sign-in',
        pathMatch: 'full'
    },
    {
        path: 'user',
        loadChildren: () => import('./user/user.routes').then(m => m.userRoutes)
    },
    {
        path: 'todo',
        loadChildren: () => import('./Todo/ToDo.routes').then(m => m.ToDoRoutes)
    },
    { path: '**', redirectTo: '/user/sign-in' },
];
