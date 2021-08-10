import { Component, Input } from '@angular/core';
import { OutputDto } from 'src/app/dto';

@Component({
  selector: 'app-output',
  templateUrl: './output.component.html',
  styleUrls: ['./output.component.scss'],
})
export class OutputComponent {
  @Input() public output!: OutputDto;
  public isInit = false;

  public addAction() {}
}
