import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CronOptions } from 'cron-editor';
import { OutputDto } from 'src/app/dto';
import { AutomationsModalComponent } from './automations-modal/automations-modal.component';

@Component({
  selector: 'app-automations',
  templateUrl: 'automations.component.html',
  styleUrls: [`./automations.component.scss`],
})
export class AutomationsComponent implements OnInit {
  @Input() public outputs: OutputDto[];
  @Input() deviceId: string;

  public cronExpression = '0 12 1W 1/1 ?';
  public isCronDisabled = false;
  public cronOptions: CronOptions = {
    formInputClass: 'form-control cron-editor-input',
    formSelectClass: 'form-control cron-editor-select',
    formRadioClass: 'cron-editor-radio',
    formCheckboxClass: 'cron-editor-checkbox',

    defaultTime: '10:00:00',
    use24HourTime: true,

    hideMinutesTab: false,
    hideHourlyTab: false,
    hideDailyTab: false,
    hideWeeklyTab: false,
    hideMonthlyTab: false,
    hideYearlyTab: true,
    hideAdvancedTab: true,

    hideSeconds: true,
    removeSeconds: true,
    removeYears: true,
  };

  constructor(public dialog: MatDialog) {}

  ngOnInit() {
    console.log(this.outputs);
  }

  public addAutomations() {
    const dialogRef = this.dialog.open(AutomationsModalComponent, {
      data: {
        outputs: this.outputs,
        deviceId: this.deviceId,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
