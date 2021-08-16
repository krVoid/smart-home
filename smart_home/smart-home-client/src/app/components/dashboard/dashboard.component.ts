import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { eventNames } from 'process';
import { of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { DeviceDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-dashboard',
  templateUrl: 'dashboard.component.html',
  styleUrls: [`./dashboard.component.scss`],
})
export class Dashboardomponent implements OnInit {
  displayedColumns: string[] = ['number', 'name', 'url', 'actions'];
  public dataSource: DeviceDto[] = [];
  public isInit = false;
  public newValue?: number;

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

  public setNewValue(deviceId: any, event: any): void {
    // do something
    this.apiService.setValue({ id: deviceId });
    event.stopPropagation();
  }
}
