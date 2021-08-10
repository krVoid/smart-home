import { Component, Input } from '@angular/core';
import { InputDto } from 'src/app/dto';

@Component({
  selector: 'app-inputs-grid',
  template: `
    <div *ngIf="isInit" class="inputs-wrapper">
      <h3>Sensors</h3>
      <table mat-table [dataSource]="dataSource" class="mat-elevation-z8">
        <ng-container matColumnDef="number">
          <th mat-header-cell *matHeaderCellDef mat-sort-header>Num.</th>
          <td mat-cell *matCellDef="let element; let i = index">{{ i + 1 }}</td>
        </ng-container>

        <ng-container matColumnDef="name">
          <th mat-header-cell *matHeaderCellDef>Name</th>
          <td mat-cell *matCellDef="let element">{{ element.name }}</td>
        </ng-container>

        <ng-container matColumnDef="description">
          <th mat-header-cell *matHeaderCellDef>Description</th>
          <td mat-cell *matCellDef="let element">
            {{ element.description }}
          </td>
        </ng-container>

        <ng-container matColumnDef="state">
          <th mat-header-cell *matHeaderCellDef>Current state</th>
          <td mat-cell *matCellDef="let element">Not implemented</td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns"></tr>
      </table>
    </div>
  `,
  styles: [
    `
      table {
        width: 100%;
        margin-top: 10px;
      }
      .inputs-wrapper {
        margin-top: 20px;
      }
    `,
  ],
})
export class InputsGridComponent {
  displayedColumns: string[] = ['number', 'name', 'description', 'state'];
  @Input() public set inputs(values: InputDto[]) {
    this.dataSource = values;
    this.isInit = this.dataSource.length > 0;
  }
  public dataSource: InputDto[] = [];
  public isInit = false;
}
