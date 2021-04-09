import { Component, OnInit } from '@angular/core';
import { AuthService } from './services';

@Component({
  selector: 'app-root',
  template: `
  <div class="atech">
    <app-navbar *ngIf="this.authService.isLoggedIn()"></app-navbar>
    <div class="atech-content">
      <router-outlet></router-outlet>
    <div>
  </div>
  `,
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'smart-home-client';
  public isLoggedIn = false;

  constructor(public authService: AuthService){}

  ngOnInit(): void {
    this.isLoggedIn = this.authService.isLoggedIn();
  }
}
