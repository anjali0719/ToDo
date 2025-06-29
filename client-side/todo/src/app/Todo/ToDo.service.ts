import { HttpClient, HttpHeaders } from "@angular/common/http"
import { Injectable } from "@angular/core"
import { Observable } from "rxjs"
import { GetTodoResponseType } from "./ToDo.model"


@Injectable({
    providedIn: 'root',
})

export class ToDoService {

    constructor(public httpClient: HttpClient){};

    createToDo(title: string, description: string, addToFav: boolean, completed: boolean, scheduledFor: Date){
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('TOKEN')}`
        })

        return this.httpClient.post('http://127.0.0.1:8000/api/vi/create-todo',
            {
                title: title,
                description: description,
                add_to_favourites: addToFav,
                completed: completed,
                scheduled_for: scheduledFor
            }, 
            {headers}
        )
    };

    getToDo(): Observable<GetTodoResponseType>{
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('TOKEN')}`
        })

        return this.httpClient.get<GetTodoResponseType>('http://127.0.0.1:8000/api/vi/get-todo', {headers})
    };
};
