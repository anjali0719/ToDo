import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { SignInResponseType, SignUpResponseType } from "./user.model";

@Injectable({
    providedIn: 'root',
})

export class UserService {

    constructor(public httpClient: HttpClient) { };

    signUp(firstName: string, lastName: string, email: string, password: string): Observable<SignUpResponseType> {

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient.post<SignUpResponseType>('http://127.0.0.1:8000/api/vi/create-user',
            {
                first_name: firstName,
                last_name: lastName,
                email,
                password
            },
            { headers }
        )
    };

    signIn(email: string, password: string): Observable<SignInResponseType> {

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return this.httpClient.post<SignInResponseType>('http://127.0.0.1:8000/api/vi/token/', { email, password }, { headers })
    };

    changePassword(oldPassword: string, newPassword: string): Observable<{ status: number; message: string }> {

        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('TOKEN')}`
        });

        return this.httpClient.put<{ status: number; message: string }>('http://127.0.0.1:8000/api/vi/change-password/',
            { 
                old_password: oldPassword, 
                new_password: newPassword 
            }, 
            { headers }
        )
    };

}
