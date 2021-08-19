import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DeviceDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-notification',
  templateUrl: `./notification.component.html`,
  styles: [``],
})
export class NotificationModalComponent {
  public modelForm: FormGroup;

  public foods = [
    { label: '==', value: 'EQUAL' },
    { label: '>=', value: 'BIGGER_OR_EQUAL' },
    { label: '<=', value: 'SMALLER_OR_EQUAL' },
    { label: '<', value: 'SMALLER' },
    { label: '>', value: 'BIGGER' },
  ];

  constructor(
    private apiService: ApiService,
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}
  ngOnInit() {
    this.modelForm = this.formBuilder.group({
      name: [''],
      description: [''],
      email: [''],
      condition: [''],
      threshold: [1],
    });
    // if (this.deviceId) {
    //   this.deviceId = this.deviceId;
    //   this.apiService.getDevice(this.deviceId).subscribe((value) => {
    //     this.modelForm.controls.name.setValue(value.name);
    //     this.modelForm.controls.url.setValue(value.url);
    //     this.device = value;
    //   });
    //   this.modelForm.disable();
    // }
  }

  get f() {
    return this.modelForm.controls;
  }

  save() {
    this.apiService
      .addNotification(
        this.modelForm.getRawValue(),
        this.data.inputId,
        this.data.deviceId
      )
      .subscribe((v) => {});
  }
}
