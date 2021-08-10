import { ActionType } from '../components/enums/action_type.enum';

export interface ActionDto {
  name: string;
  description?: string;
  url: string;
  parameters?: string[];
  type: ActionType;
  id: string;
}
