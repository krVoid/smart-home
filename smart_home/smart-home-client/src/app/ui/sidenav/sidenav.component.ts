import { Component, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { MatDrawer } from '@angular/material/sidenav';

@Component({
  selector: 'app-sidenav',
  template: `
    <mat-drawer-container class="sidenav-container" autosize>
      <mat-drawer #drawer class="sidenav" mode="side">
        <p class="sidenav-header">MENU</p>
        <p class="sidenav-element" routerLink="/blocks">Blocks</p>
        <p class="sidenav-element" routerLink="/transations">
          Pending transactions
        </p>
        <p class="sidenav-element" routerLink="/keys">Keys</p>
        <p class="sidenav-element" routerLink="/account-balance">
          Account balance
        </p>
        <p class="sidenav-element" routerLink="/network">Network nodes</p>
      </mat-drawer>
      <div class="sidenav-content">
        <ng-content></ng-content>
      </div>
    </mat-drawer-container>
  `,
  styleUrls: ['sidenav.component.scss'],
})
export class SidenavComponent {
  @ViewChild('drawer') drawer: MatDrawer;

  constructor(private router: Router) {}
}
