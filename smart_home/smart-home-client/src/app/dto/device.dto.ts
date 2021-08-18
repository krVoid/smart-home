import { ActionDto } from './action.dto';

export interface DeviceDto {
  url: string;
  name: string;
  deviceinput?: InputDto[];
  deviceoutput?: OutputDto[];
  id: number;
}

export interface InputDto {
  name: string;
  description?: string;
  id: number;
  inputId: any;
}

export interface OutputDto {
  name: string;
  outputId: any;
  description?: string;
  isBinary: boolean;
  min?: number;
  max?: number;
  id: number;
  outputaction: ActionDto[];
}
