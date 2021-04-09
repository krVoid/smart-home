import { Component, Output, EventEmitter } from "@angular/core";
import { Router } from "@angular/router";
import { AuthService } from "src/app/services";

@Component({
  selector: "app-navbar",
  template: `
    <div class="navbar">
      <div class="navbar-icons">
        <i class="navbar-right fa fa-user" >
        </i>
        <h3 class="navbar-right" (click)="logout()">Logout</h3>
        <i
          class="navbar-left fa fa-home" (click)="navigateToHome()"
        ></i>
      </div>
    </div>
  `,
  styleUrls: ["navbar.component.scss"],
})
export class NavbarComponent {
  constructor(private router: Router, private authService: AuthService) {}

  public navigateToHome(): void {
    this.router.navigate([""]);
  }

  public logout(): void {    
    this.authService.logout().subscribe(success => {
      if (success) {
        this.router.navigate(['/login']);
      }
    });
  }
}
