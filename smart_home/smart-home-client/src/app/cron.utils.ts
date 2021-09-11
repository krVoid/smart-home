import { Pipe, PipeTransform } from '@angular/core';
import cronstrue from 'cronstrue';

export function cronExpression(value: string, lang: string = 'en-us'): string {
  const resultLang = lang.split('-')[0];
  let result = value;
  try {
    result = cronstrue.toString(value, { locale: resultLang });
  } catch (error) {
    return result;
  }
  return result.includes('undefined') || result.includes('null')
    ? value
    : result;
}

@Pipe({ name: 'cronPipe' })
export class CronPipe implements PipeTransform {
  public transform(cronString?: string | null, lang?: string): string | null {
    if (!cronString) {
      return null;
    }
    const result = cronExpression(cronString, lang);
    return result === cronString ? '' : result;
  }
}
