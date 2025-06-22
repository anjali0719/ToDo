export interface SignUpRequestType {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
}

export interface SignUpResponseType {
    first_name: string;
    last_name: string;
    email: string;
    is_active: boolean | null;
}

export interface SignInResponseType {
    access_token: string; 
    token_type: string;
}
