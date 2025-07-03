import { HttpClient, HttpHeaders } from "@angular/common/http"
import { Injectable } from "@angular/core"
import { Observable } from "rxjs"
import { GetTodoResponseType } from "./ToDo.model"


@Injectable({
    providedIn: 'root',
})

export class ToDoService {

    constructor(public httpClient: HttpClient) { };

    createToDo(title: string, description: string, addToFav: boolean, completed: boolean, scheduledFor: string) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('TOKEN')}`
        })

        return this.httpClient.post(`http://127.0.0.1:8000/api/vi/create-todo/`,
            {
                title: title,
                description: description,
                add_to_favourites: addToFav,
                completed: completed,
                scheduled_for: scheduledFor
            },
            { headers }
        )
    };

    toDoList(search: string, filterType: string): Observable<GetTodoResponseType> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('TOKEN')}`
        })

        return this.httpClient.get<GetTodoResponseType>(`http://127.0.0.1:8000/api/vi/todo-list?search=${search ?? ''}&filter_type=${filterType}&limit=${10}&offset=${0}`, { headers })
    };

    updateToDo(toDoId: number, title: string, description: string, addToFav: boolean, completed: boolean, scheduledFor: string) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('TOKEN')}`
        })

        return this.httpClient.put(
            `http://127.0.0.1:8000/api/vi/update-todo/${toDoId}/`,
            {
                title: title,
                description: description,
                add_to_favourites: addToFav,
                completed: completed,
                scheduled_for: scheduledFor,
            },
            { headers }
        )
    };

    deleteToDo(toDoId: number): Observable<{ status: number, message: string }> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('TOKEN')}`
        })

        return this.httpClient.delete<{ status: number, message: string }>(
            `http://127.0.0.1:8000/api/vi/delete-todo/?todo_id=${toDoId}`,
            { headers },
        )
    };
};
