import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { UserDto } from 'src/app/dto';
import { ApiService, AuthService } from 'src/app/services';

@Component({
  selector: 'app-admin',
  template: `
  Admin Dashboard

  <table *ngIf="isInit" mat-table [dataSource]="dataSource" class="mat-elevation-z8">
  
  <ng-container matColumnDef="number">
    <th mat-header-cell *matHeaderCellDef mat-sort-header> Num. </th>
    <td mat-cell *matCellDef="let element; let i = index">{{i + 1}}</td>
  </ng-container>

  <ng-container matColumnDef="username">
    <th mat-header-cell *matHeaderCellDef> Username </th>
    <td mat-cell *matCellDef="let element"> {{element.username}} </td>
  </ng-container>

  <ng-container matColumnDef="email">
    <th mat-header-cell *matHeaderCellDef> email </th>
    <td mat-cell *matCellDef="let element"> {{element.email}} </td>
  </ng-container>


  <ng-container matColumnDef="first_name">
    <th mat-header-cell *matHeaderCellDef> First name </th>
    <td mat-cell *matCellDef="let element"> {{element.first_name}} </td>
  </ng-container>

  <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
  <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
</table>
`,
  styles: [`
  table {
    width: 100%;
  }
  `]
})
export class AdminDashboardComponent {
    displayedColumns: string[] = ['number','username', 'email','first_name'];
    public dataSource: UserDto[] = [];
    public isInit = false;
    constructor(private apiService: AuthService, private router: Router){        
    }

    public ngOnInit(): void {
        this.apiService.getUsers().pipe(
          catchError(error => {
            alert(error.error);
            return of([]);
          })).subscribe(v => { this.isInit = true; this.dataSource = v});
    }
}
