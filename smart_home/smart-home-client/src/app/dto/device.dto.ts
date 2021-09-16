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
  inputnotification?: any[];
}

export interface OutputDto {
  name: string;
  outputId: any;
  description?: string;
  isBinary: boolean;
  isColorPicker?: boolean;
  min?: number;
  max?: number;
  id: number;
  outputaction: ActionDto[];
  outputautomation?: any[];
}
