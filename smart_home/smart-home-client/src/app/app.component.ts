import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { AuthService } from './services';
import { SidenavComponent } from './ui';

@Component({
  selector: 'app-root',
  template: `
    <div class="atech">
      <app-navbar
        (toggleMenu)="toggle()"
        *ngIf="this.authService.isLoggedIn()"
      ></app-navbar>
      <div class="atech-content">
        <app-sidenav #sidenav> <router-outlet></router-outlet></app-sidenav>
      </div>
      <div></div>
    </div>
  `,
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  title = 'smart-home-client';
  public isLoggedIn = false;
  @ViewChild('sidenav') sidenav: SidenavComponent;

  constructor(public authService: AuthService) {}

  ngOnInit(): void {
    this.isLoggedIn = this.authService.isLoggedIn();
  }

  public toggle(): void {
    this.sidenav.drawer.toggle();
  }
}
