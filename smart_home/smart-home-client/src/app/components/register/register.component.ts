import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services';

@Component({
  selector: 'app-register',
  template: `
  <div class="header center">Register</div>
  <form [formGroup]="registerForm" (ngSubmit)="register()">

    <mat-form-field>
      <input matInput type="text" id="username" placeholder="Username" autocomplete="off" formControlName="username" required>
    </mat-form-field>

    <mat-form-field>
      <input matInput type="text" id="email" placeholder="Email" autocomplete="off" formControlName="email" required>
    </mat-form-field>

    <mat-form-field>
      <input matInput type="password" id="password" placeholder="Password" formControlName="password" required>
    </mat-form-field>

    <mat-form-field>
      <input matInput type="password" id="password2" placeholder="Confirm Password" formControlName="password2" required>
      <mat-error *ngIf="registerForm.hasError('notSame')">
        Passwords do not match
      </mat-error> 
    </mat-form-field>

    <div class="actions">
      <button mat-raised-button color="primary" type="submit" [disabled]="!registerForm.valid">Register</button>
      <br /><br />
      <div class="header center">If you have already account</div>
      <button mat-raised-button color="primary" (click)="navigateToLogin()">Login</button>
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
export class RegisterComponent {

  registerForm: FormGroup;

  constructor(private authService: AuthService, private formBuilder: FormBuilder, private router: Router) { }

  ngOnInit() {
    this.registerForm = this.formBuilder.group({
      username: [''],
      email: [''],
      password: ['', {validators: Validators.minLength(8)}],
      password2: ['', {validators: Validators.minLength(8)}]
    }, {validator: this.checkPasswords });
  }

  get f() { return this.registerForm.controls; }

  register() {
    this.authService.register(
      {
        username: this.f.username.value,
        password: this.f.password.value,
        email: this.f.email.value
      }
    )
    .subscribe(success => {
      if (success) {
        this.router.navigate(['/dashboard']);
      }
    });
  }
  navigateToLogin() {
    this.router.navigate(['/login'])
  }

  checkPasswords(group: FormGroup) { 
    let pass = group.get('password').value;
    let confirmPass = group.get('password2').value;

    return pass === confirmPass ? null : { notSame: true }     
  }
}
