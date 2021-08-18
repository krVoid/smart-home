import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DeviceDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-device-details',
  template: `
    <h2 class="header center">Module</h2>
    <form [formGroup]="modelForm">
      <mat-form-field>
        <input
          matInput
          type="text"
          id="name"
          placeholder="name"
          autocomplete="off"
          formControlName="name"
          required
        />
      </mat-form-field>

      <mat-form-field>
        <input
          matInput
          id="url"
          placeholder="url"
          formControlName="url"
          required
        />
      </mat-form-field>
      <button mat-raised-button color="primary" (click)="register()">
        {{ deviceId ? 'Update' : 'Register' }}
      </button>
    </form>

    <div *ngIf="device && device.deviceoutput">
      <app-output
        *ngFor="let outputValue of device.deviceoutput"
        [output]="outputValue"
        [deviceId]="device.id"
      ></app-output>
    </div>

    <div *ngIf="device && device.deviceinput">
      <app-input
        *ngFor="let inputValue of device.deviceinput"
        [input]="inputValue"
        [deviceId]="device.id"
      ></app-input>
    </div>

    <!--   <app-outputs-grid
      *ngIf="device && device.deviceoutput"
      [outputs]="device.deviceoutput"
    ></app-outputs-grid> -->
    <!--    <app-actions></app-actions>
 <app-inputs-grid
      *ngIf="device && device.deviceinput"
      [inputs]="device.deviceinput"
    ></app-inputs-grid>
    {{ device | json }} -->
  `,
  styles: [
    `
      :host {
        text-align: center;
        display: block;
        margin-top: 30px;
      }

      form {
        max-width: 300px;
        margin: auto;
      }

      mat-form-field {
        width: 100%;
      }

      .actions {
        text-align: center;
      }
    `,
  ],
})
export class DeviceDetailsComponent {
  public modelForm: FormGroup;
  public deviceId?: string;
  public device?: DeviceDto;

  constructor(
    private apiService: ApiService,
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute
  ) {}
  ngOnInit() {
    this.modelForm = this.formBuilder.group({
      name: [''],
      url: [''],
    });
    this.deviceId = this.route.snapshot.params.id;
    if (this.deviceId) {
      this.deviceId = this.deviceId;
      this.apiService.getDevice(this.deviceId).subscribe((value) => {
        this.modelForm.controls.name.setValue(value.name);
        this.modelForm.controls.url.setValue(value.url);
        this.device = value;
      });
      this.modelForm.disable();
    }
  }

  get f() {
    return this.modelForm.controls;
  }

  navigateToRegister() {
    this.router.navigate(['/register']);
  }

  register() {
    if (this.deviceId) {
      this.apiService.updateDevices({ id: this.deviceId }).subscribe((v) => {
        let currentUrl = this.router.url;
        this.router
          .navigateByUrl('/', { skipLocationChange: true })
          .then(() => {
            this.router.navigate([currentUrl]);
          });
      });
    } else {
      this.apiService
        .registerDevices(this.modelForm.getRawValue())
        .subscribe((v) => {
          this.router.navigate(['device/', v]);
        });
    }
  }
}
