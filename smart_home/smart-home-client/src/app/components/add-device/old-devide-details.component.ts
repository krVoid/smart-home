import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-old-device-details',
  template: `
  <div class="header center">Device Control</div>
  <form [formGroup]="modelForm">

    <mat-form-field>
      <input matInput type="text" id="name" placeholder="name" autocomplete="off" formControlName="name" required>
    </mat-form-field>

    <mat-form-field>
      <input matInput id="url" placeholder="url" formControlName="url" required>
    </mat-form-field>
    </form>
    <div class="actions">
      <mat-slide-toggle color="primary" (click)="switchLamp()" [checked]="turnOnOff">Switch Lamp</mat-slide-toggle>
      <br /><br />
      <mat-form-field style="width: 300px !important; margin: auto;" >
      <input matInput  placeholder="Set value from 0-255" [(ngModel)]="newIlluminance" >
    </mat-form-field>
      <div class="header center"></div>
      <button mat-raised-button color="primary" (click)="setNewIlluminance()">Set new Illuminance</button><br /><br />
      <mat-slide-toggle (click)="setAutoLamp()"
      [checked]="isAutoLamp">
      SetAuto Lamp
  </mat-slide-toggle>
    </div>
 `,
  styles: [`
  :host {
    text-align: center;
    display: block;
    margin-top: 30%;
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
  `]
})
export class OldDeviceDetailsComponent {
 public newIlluminance = 0;
 public isAutoLamp = false;
  modelForm: FormGroup;
  turnOnOff = false;
  constructor(private apiService: ApiService, private formBuilder: FormBuilder, private router: Router, private route: ActivatedRoute) { }
  deviceId = '';
  ngOnInit() {
    this.modelForm = this.formBuilder.group({
      name: [{value: '', disabled: true}],
      url: [{value: '', disabled: true}]
    });

    this.route.params.subscribe(params => {
      this.deviceId = params.id
      this.apiService.getDevice(params.id).subscribe(value => {
        this.modelForm.controls.name.setValue(value.name)
        this.modelForm.controls.url.setValue(value.url)
      })
    })
  }

  get f() { return this.modelForm.controls; }

  navigateToRegister() {
    this.router.navigate(['/register'])
  }
  switchLamp() {
    this.turnOnOff = !this.turnOnOff;
    if(this.deviceId) {
      this.apiService.switchLamp({id: this.deviceId, state: this.turnOnOff}).subscribe(v=> console.log(v)
      );
    }
  }
  setNewIlluminance(){
    if(this.deviceId) {
      this.apiService.setIlluminanceOnLamp({id: this.deviceId, state: this.newIlluminance}).subscribe(v=> console.log(v)
      );
    }  
  }
  setAutoLamp() {
    this.isAutoLamp = !this.isAutoLamp
    if(this.deviceId) {
      this.apiService.setAutoLamp({id: this.deviceId, state: this.isAutoLamp}).subscribe(v=> console.log(v)
      );
    }
    if(!this.isAutoLamp) {
      this.turnOnOff = false;
      this.switchLamp();
    } else {
      this.turnOnOff = true;
    }
  }
}
