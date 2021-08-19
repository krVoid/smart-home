import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { OutputDto } from 'src/app/dto';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-output',
  templateUrl: './output.component.html',
  styleUrls: ['./output.component.scss'],
})
export class OutputComponent implements OnInit {
  @Input() public output!: OutputDto;
  @Input() public deviceId: any;
  public isInit = false;
  public newValue?: number;
  public turnOn = false;

  constructor(private apiService: ApiService, private router: Router) {}

  async ngOnInit() {
    const t = await this.apiService.getOtuputValue({
      id: this.deviceId,
      outputId: this.output.outputId,
    });
    console.log(t);
  }

  public addAction() {}
  public async setNewValue(event: any): Promise<void> {
    // do something
    await this.apiService.setValue({
      id: this.deviceId,
      outputId: this.output.outputId,
      value: this.newValue,
    });
    event.stopPropagation();
  }

  public async turnOnOutput(): Promise<void> {
    await this.apiService.turnOn({
      id: this.deviceId,
      outputId: this.output.outputId,
    });
  }

  public async toggleOutput(event: any): Promise<void> {
    console.log(event);

    if (event) {
      await this.apiService.turnOn({
        id: this.deviceId,
        outputId: this.output.outputId,
      });
    } else {
      await this.apiService.turnOff({
        id: this.deviceId,
        outputId: this.output.outputId,
      });
    }
  }
}
