import { Component, Input } from '@angular/core';
import { OutputDto } from 'src/app/dto';

@Component({
  selector: 'app-actions',
  template: `
    <div>
      <div>
        <h3>Advanced actions</h3>

        <button
          type="button"
          class="add-puch__icon"
          (click)="addAction()"
          data-toggle="tooltip"
          data-placement="top"
          title="Add action"
        >
          <i class="fa fa-plus"></i>
        </button>
      </div>
      <div>
        <mat-accordion>
          <mat-expansion-panel hideToggle>
            <mat-expansion-panel-header>
              <mat-panel-title>
                <mat-slide-toggle [checked]="isAutoLamp">
                  Set Auto Lamp
                </mat-slide-toggle>
              </mat-panel-title>
            </mat-expansion-panel-header>
            <div class="action-textarea">
              <strong>def custom_func(inputs, outputs):</strong>
              <textarea></textarea>

              <strong> return outputs</strong>
            </div>
          </mat-expansion-panel>
        </mat-accordion>
      </div>
    </div>
  `,
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
export class AdvancedActionsComponent {
  public isAutoLamp = false;
}
