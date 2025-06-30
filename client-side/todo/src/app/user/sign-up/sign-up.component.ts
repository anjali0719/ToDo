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
import { SignUpResponseType } from '../user.model';


@Component({
  selector: 'app-sign-up',
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
    RouterLink
  ],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.less'
})
export class SignUpComponent {

  constructor(
    public userService: UserService,
    public router: Router
  ) { };

  user: SignUpResponseType | undefined;

  signInForm = new FormGroup({
    firstName: new FormControl('', Validators.required),
    lastName: new FormControl('', Validators.required),
    email: new FormControl('', Validators.email),
    password: new FormControl('', Validators.required)
  });

  onCreateAccount() {
    this.userService.signUp(this.signInForm.value.firstName!, this.signInForm.value.lastName!, this.signInForm.value.email!, this.signInForm.value.password!).subscribe({
      next: (response: SignUpResponseType) => {
        this.user = response;
        localStorage.setItem("EMAIL", response.email)
        this.router.navigate(['/user/sign-in/'])
      },
      error: error => console.log(`Error: ${error}`)
    })
    this.signInForm.reset()
  };

}
