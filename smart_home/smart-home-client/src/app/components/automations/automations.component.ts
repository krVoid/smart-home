import { Component, Input } from '@angular/core';
import { CronOptions } from 'cron-editor';

@Component({
  selector: 'app-automations',
  templateUrl: 'automations.component.html',
  styleUrls: [`./automations.component.scss`],
})
export class AutomationsComponent {
  @Input() public outputs: any[];

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
    hideYearlyTab: false,
    hideAdvancedTab: false,

    hideSeconds: true,
    removeSeconds: true,
    removeYears: true,
  };
}
