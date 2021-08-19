import { Component, Input, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subject, timer } from 'rxjs';
import { concatMap, takeUntil } from 'rxjs/operators';
import { InputDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';
import { MatDialog } from '@angular/material/dialog';
import { NotificationModalComponent } from './notification/notification.component';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss'],
})
export class InputComponent implements OnDestroy {
  @Input() public input!: InputDto;
  @Input() public deviceId: any;
  public isInit = false;
  public newValue?: number;
  public showCurrentStatus = false;
  public currentStatus: any = 0;
  private destroyPolling$: Subject<void> = new Subject();

  constructor(
    public dialog: MatDialog,
    private apiService: ApiService,
    private router: Router
  ) {}

  public async toogleShowStatus(event: any): Promise<void> {
    console.log(event);

    if (event) {
      timer(0, 2000)
        .pipe(
          concatMap(() =>
            this.apiService.getInputValue({
              id: this.deviceId,
              inputId: this.input.inputId,
            })
          ),
          takeUntil(this.destroyPolling$)
        )
        .subscribe((result) => {
          this.currentStatus = result;
        });
    } else {
      this.destroyPolling$.next();
    }
  }

  public addNotification(input: InputDto): void {
    const dialogRef = this.dialog.open(NotificationModalComponent, {
      data: {
        inputId: this.input.inputId,
        deviceId: this.deviceId,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log(`Dialog result: ${result}`);
    });
  }

  public ngOnDestroy(): void {
    this.destroyPolling$.next();
    this.destroyPolling$.complete();
  }
}
