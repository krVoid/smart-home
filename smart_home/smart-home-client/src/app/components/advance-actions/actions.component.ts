import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { OutputDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-actions',
  templateUrl: './actions.component.html',
  styles: [
    `
      .action-textarea {
        display: flex;
        flex-direction: column;
        text-align: left;
      }
      .inputs-wrapper {
        margin-top: 40px;
      }
      .add-puch__icon {
        padding: 0px 5px;
        border-radius: 50%;
        border: 3px solid #a9aaab;
        box-shadow: 0px 0px 8px #888;
        font-size: 10px;
        color: #a9aaab;
        height: 24px;
        cursor: pointer;
        floar: right;
      }

      button.add-puch__icon:hover {
        transform: translateY(-2px) scale(1.008);
        box-shadow: 0 0px 8px #3565a6;
      }
    `,
  ],
})
export class AdvancedActionsComponent implements OnInit {
  @Input() device!: any;
  public modelForm: FormGroup;
  public isAutoLamp = false;
  public addAction(): void {}

  constructor(
    private apiService: ApiService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    if (this.device.deviceaction) {
      console.log(this.device);
      this.modelForm = this.formBuilder.group({
        name: [this.device.deviceaction[0].name],
        description: [this.device.deviceaction[0].description],
        isTurnOn: [this.device.deviceaction[0].isTurnOn],
        inputs: [this.device.deviceaction[0].inputs],
        outputs: [this.device.deviceaction[0].outputs],
        content: [this.device.deviceaction[0].content],
      });
    } else {
      this.modelForm = this.formBuilder.group({
        name: [''],
        description: [''],
        isTurnOn: [false],
        inputs: [''],
        outputs: [''],
        content: [''],
      });
    }
  }

  public onSave(): void {
    if (!this.device.deviceaction) {
      this.apiService
        .createAction(this.device.id, this.modelForm.getRawValue())
        .then(() => {});
    } else {
      this.apiService
        .editAction(
          this.device.id,
          this.device.deviceaction[0].id,
          this.modelForm.getRawValue()
        )
        .then(() => {});
    }
  }
}
