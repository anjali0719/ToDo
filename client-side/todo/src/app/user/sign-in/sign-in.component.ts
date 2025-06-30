import { Component } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import {
  TuiAppearance,
  TuiButton,
  TuiError,
  TuiIcon,
  TuiLink,
  TuiTextfield,
  TuiTitle,
} from '@taiga-ui/core';
import { TuiFieldErrorPipe, TuiPassword } from '@taiga-ui/kit';
import { TuiCardLarge, TuiForm, TuiHeader } from '@taiga-ui/layout';
import { Router, RouterLink } from '@angular/router';
import { UserService } from '../user.service';
import { SignInResponseType } from '../user.model';


@Component({
  selector: 'app-sign-in',
  imports: [
    AsyncPipe,
    ReactiveFormsModule,
    TuiAppearance,
    TuiButton,
    TuiCardLarge,
    TuiError,
    TuiFieldErrorPipe,
    TuiForm,
    TuiHeader,
    TuiTextfield,
    TuiTitle,
    TuiPassword,
    TuiIcon,
    TuiLink,
    RouterLink,
  ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.less'
})
export class SignInComponent {

  constructor(
    public userService: UserService,
    public router: Router,
  ) { };


  loginToken: SignInResponseType | undefined;

  signInForm = new FormGroup({
    email: new FormControl('', Validators.email),
    password: new FormControl('', Validators.required)
  });

  onLogin() {
    this.userService.signIn(this.signInForm.value.email!, this.signInForm.value.password!).subscribe({
      next: (response: SignInResponseType) => {
        this.loginToken = response;
        localStorage.setItem("TOKEN", response.access_token)
        this.router.navigate(['/todo/todo-dashboard/'])
      },
      error: error => console.log(`Error in SignIn: ${error}`)
    })
    this.signInForm.reset()
  };

}
