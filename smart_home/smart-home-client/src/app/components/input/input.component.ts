import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { throwMatDuplicatedDrawerError } from '@angular/material/sidenav';
import { Router } from '@angular/router';
import { Subject, timer } from 'rxjs';
import { concatMap, takeUntil } from 'rxjs/operators';
import { InputDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';

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

  constructor(private apiService: ApiService, private router: Router) {}

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

  public ngOnDestroy(): void {
    this.destroyPolling$.next();
    this.destroyPolling$.complete();
  }
}
