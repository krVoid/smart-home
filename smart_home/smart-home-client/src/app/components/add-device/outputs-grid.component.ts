import { Component, Input } from '@angular/core';
import { OutputDto } from 'src/app/dto';

@Component({
  selector: 'app-outputs-grid',
  template: `
    <div *ngIf="isInit" class="inputs-wrapper">
      <h3>Devices</h3>
      <mat-accordion>
        <mat-expansion-panel hideToggle *ngFor="let outputValue of dataSource">
          <mat-expansion-panel-header>
            <mat-panel-title> {{ outputValue.name }} </mat-panel-title>
            <mat-panel-description>
              {{ outputValue.description }}
            </mat-panel-description>
          </mat-expansion-panel-header>
          <p>This is the primary content of the panel.</p>
        </mat-expansion-panel>
      </mat-accordion>
    </div>
  `,
  styles: [
    `
      .inputs-wrapper {
        margin-top: 40px;
      }
    `,
  ],
})
export class OutputsGridComponent {
  @Input() public set outputs(values: OutputDto[]) {
    this.dataSource = values;
    console.log(values);
    this.isInit = this.dataSource.length > 0;
  }
  public dataSource: OutputDto[] = [];
  public isInit = false;
}
