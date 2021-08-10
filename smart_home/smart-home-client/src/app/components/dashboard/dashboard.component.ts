import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { DeviceDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-dashboard',
  templateUrl: 'dashboard.component.html',
  styles: [
    `
  table {
    width: 100%;
    margin-top: 10px;
  }
  .button
  `,
  ],
})
export class Dashboardomponent implements OnInit {
  displayedColumns: string[] = ['number', 'name', 'url', 'actions'];
  public dataSource: DeviceDto[] = [];
  public isInit = false;
  constructor(private apiService: ApiService, private router: Router) {}

  public ngOnInit(): void {
    this.apiService
      .getDevices()
      .pipe(
        catchError((error) => {
          alert(error.error);
          return of([]);
        })
      )
      .subscribe((v) => {
        this.isInit = true;
        this.dataSource = v;
      });
  }

  public navigateToDetails(id: string): void {
    this.router.navigate(['device/', id]);
  }
  public navigateToAdd(): void {
    this.router.navigate(['device/']);
  }
}
