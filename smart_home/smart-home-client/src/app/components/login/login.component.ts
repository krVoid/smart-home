import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services';

@Component({
  selector: 'app-login',
  template: `
  <div class="header center">Log In</div>
  <form [formGroup]="loginForm" (ngSubmit)="login()">

    <mat-form-field>
      <input matInput type="text" id="username" placeholder="Username" autocomplete="off" formControlName="username" required>
    </mat-form-field>

    <mat-form-field>
      <input matInput type="password" id="password" placeholder="Password" formControlName="password" required>
    </mat-form-field>

    <div class="actions">
      <button mat-raised-button color="primary" type="submit" [disabled]="!loginForm.valid">LOG IN</button>
      <br /><br />
      <div class="header center">Or if you do not have account</div>
      <button mat-raised-button color="primary" (click)="navigateToRegister()">Register Now</button>
    </div>
  </form>`,
  styles: [`
  :host {
    text-align: center;
    display: block;
    margin-top: 30%;
  }
  
  form {
    max-width: 300px;
    margin: auto;
  }
  
  mat-form-field {
    width: 100%;
  }
  
  .actions {
    text-align: center;
  }
  `]
})
export class LoginComponent {

  loginForm: FormGroup;

  constructor(private authService: AuthService, private formBuilder: FormBuilder, private router: Router) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: [''],
      password: ['']
    });
  }

  get f() { return this.loginForm.controls; }

  login() {
    this.authService.login(
      {
        username: this.f.username.value,
        password: this.f.password.value
      }
    )
    .subscribe(success => {
      if (success) {
        this.router.navigate(['/dashboard']);
      }
    });
  }

  navigateToRegister() {
    this.router.navigate(['/register'])
  }
}
