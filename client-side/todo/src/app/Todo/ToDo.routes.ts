import { Routes } from "@angular/router";

export const ToDoRoutes: Routes = [
    {
        path: 'todo-dashboard',
        loadComponent: () => import('./todo-dashboard/todo-dashboard.component').then(m => m.TodoDashboardComponent),
        data: {
            title: 'ToDo Dashboard'
        }
    }
];
