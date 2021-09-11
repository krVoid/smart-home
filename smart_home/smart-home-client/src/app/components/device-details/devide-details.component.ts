import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DeviceDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';
import { smartHomeIcons } from 'src/app/utils';

@Component({
  selector: 'app-device-details',
  templateUrl: './device-details.component.html',
  styleUrls: ['./device-details.component.scss'],
})
export class DeviceDetailsComponent {
  public modelForm: FormGroup;
  public deviceId?: string;
  public device?: DeviceDto;
  public iconstOptions = smartHomeIcons;

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
      isSmartLight: [false],
      isAutoTurnOn: [false],
      isAutoAirConditioner: [false],
      iconName: [''],
      imageSrc: [''],
    });
    this.deviceId = this.route.snapshot.params.id;
    if (this.deviceId) {
      this.deviceId = this.deviceId;
      this.apiService.getDevice(this.deviceId).subscribe((value) => {
        this.device = value;
        this.modelForm.controls.name.setValue(value.name);
        this.modelForm.controls.url.setValue(value.url);
        this.modelForm.controls.name.disable();
        this.modelForm.controls.url.disable();
        this.modelForm.controls.isSmartLight.setValue(value.isSmartLight);
        this.modelForm.controls.isAutoTurnOn.setValue(value.isAutoTurnOn);
        this.modelForm.controls.iconName.setValue(value.iconName);
      });
      // this.modelForm.disable();
    }
  }

  get f() {
    return this.modelForm.controls;
  }

  navigateToRegister() {
    this.router.navigate(['/register']);
  }
  onFileChanged(event: any) {
    const selectedFile = <File>event.target.files[0];
    console.log(selectedFile);
    // this.modelForm.controls.image.setValue(selectedFile);
    var reader = new FileReader();

    console.log(event);
  }
  // _handleReaderLoaded(e) {
  //   let reader = e.target;
  //   this.imageSrc = reader.result;
  //   console.log(this.imageSrc)
  // }
  register() {
    console.log(this.modelForm.getRawValue());
    if (this.deviceId) {
      this.apiService
        .updateDevices({ ...this.modelForm.getRawValue(), id: this.deviceId })
        .subscribe((v) => {
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
  switchLamp() {
    if (this.deviceId) {
      if (this.modelForm.controls.isAutoAirConditioner) {
      } else {
        this.apiService
          .setAutoLamp({
            id: this.deviceId,
            state: this.modelForm.controls.isAutoTurnOn.value,
          })
          .subscribe((v) => console.log(v));
      }
    }
  }
}
