import { Component, Inject, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { CronOptions } from 'cron-editor';
import { OutputDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-automations-modal',
  templateUrl: 'automations-modal.component.html',
})
export class AutomationsModalComponent implements OnInit {
  public modelForm: FormGroup;

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

  public selectedOutput?: OutputDto;
  constructor(
    private apiService: ApiService,
    private formBuilder: FormBuilder,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}
  ngOnInit() {
    this.modelForm = this.formBuilder.group({
      output: [''],
      newValue: [''],
      turnOn: [''],
    });

    this.modelForm.controls.output.valueChanges.subscribe((outputId) => {
      console.log(outputId);
      this.selectedOutput = this.data.outputs.find(
        (otuput) => otuput.id === outputId
      );
    });
    console.log(this.data);
  }
  get f() {
    return this.modelForm.controls;
  }

  save() {
    if (this.selectedOutput) {
      this.apiService
        .addAutomation(
          { ...this.modelForm.getRawValue(), cron: this.cronExpression },
          this.selectedOutput.outputId,
          this.data.deviceId
        )
        .subscribe((v) => {});
    }
  }
}
