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
  TuiTextfield,
  TuiTitle,
} from '@taiga-ui/core';
import { TuiFieldErrorPipe, TuiPassword } from '@taiga-ui/kit';
import { TuiCardLarge, TuiForm, TuiHeader } from '@taiga-ui/layout';
import { UserService } from '../../user.service';


@Component({
  selector: 'app-change-password',
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
    TuiIcon
  ],
  templateUrl: './change-password.component.html',
  styleUrl: './change-password.component.less'
})
export class ChangePasswordComponent {

  constructor(public userService: UserService) { };

  changePasswordForm = new FormGroup({
    oldPassword: new FormControl('', Validators.required),
    newPassword: new FormControl('', Validators.required)
  });

  onChangePassword() {
    this.userService.changePassword(this.changePasswordForm.value.oldPassword!, this.changePasswordForm.value.newPassword!).subscribe({
      next: (response: { status: number; message: string }) => {
        console.log(response.message);
      },
      error: error => console.log(`Error in Changing Password: ${error}`)
    });
  };

}
