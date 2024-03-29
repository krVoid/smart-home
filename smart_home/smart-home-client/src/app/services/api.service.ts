import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { DeviceDto } from '../dto';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private readonly apiUrl = 'http://localhost:8000/api';
  private loggedUser: string;

  constructor(private http: HttpClient) {}

  //----color picker----
  public setRedValue(switchL: any): Promise<boolean> {
    return this.http
      .post<any>(`${this.apiUrl}/set_value/red/`, switchL)
      .toPromise();
  }

  public setGreenValue(switchL: any): Promise<boolean> {
    return this.http
      .post<any>(`${this.apiUrl}/set_value/green/`, switchL)
      .toPromise();
  }

  public setBlueValue(switchL: any): Promise<boolean> {
    return this.http
      .post<any>(`${this.apiUrl}/set_value/blue/`, switchL)
      .toPromise();
  }

  //-----------------------------

  public getDevices(): Observable<DeviceDto[]> {
    return this.http.get<any>(`${this.apiUrl}/devicedevice/`);
  }

  public getDevice(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/devicedevice/${id}/`);
  }
  public registerDevices(newDevice: any): Observable<boolean> {
    console.log(newDevice);
    let headers = new HttpHeaders();
    // headers = headers.set('Content-Type', 'multipart/form-data');
    headers.append('Accept', 'application/json');

    return this.http.post<any>(`${this.apiUrl}/register_device/`, newDevice, {
      headers,
      reportProgress: true,
    });
  }
  public updateDevices(newDevice: any): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/update_device/`, newDevice);
  }

  public turnOn(switchL: any): Promise<boolean> {
    console.log(switchL);

    return this.http.post<any>(`${this.apiUrl}/turn_on/`, switchL).toPromise();
  }
  public turnOff(switchL: any): Promise<boolean> {
    return this.http.post<any>(`${this.apiUrl}/turn_off/`, switchL).toPromise();
  }
  public setValue(switchL: any): Promise<boolean> {
    return this.http
      .post<any>(`${this.apiUrl}/set_value/`, switchL)
      .toPromise();
  }

  public createAction(deviceId: any, data: any): Promise<any> {
    return this.http
      .post<any>(`${this.apiUrl}/device/${deviceId}/action`, data)
      .toPromise();
  }

  public getDeviceActions(deviceId: any) {
    return this.http.get<any>(`${this.apiUrl}/device/${deviceId}/action`);
  }

  public editAction(deviceId: any, actionID: any, data: any): Promise<any> {
    return this.http
      .put<any>(`${this.apiUrl}/device/${deviceId}/action/${actionID}`, data)
      .toPromise();
  }

  //notification
  public addNotification(
    newNotification: any,
    inputId: any,
    deviceId: any
  ): Observable<any> {
    return this.http.post<any>(
      `${this.apiUrl}/device/${deviceId}/input/${inputId}/notification`,
      newNotification
    );
  }

  public addAutomation(
    newNotification: any,
    inputId: any,
    deviceId: any
  ): Observable<any> {
    return this.http.post<any>(
      `${this.apiUrl}/device/${deviceId}/output/${inputId}/automations`,
      newNotification
    );
  }

  //to testing
  public getOtuputValue(switchL: any): Promise<boolean> {
    return this.http
      .post<any>(`${this.apiUrl}/get_output_value`, switchL)
      .toPromise();
  }
  public getInputValue(switchL: any): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/get_input_value`, switchL);
  }

  //this is old functions pls don't move
  public addDevices(newDevice: DeviceDto): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/devicedevice/`, newDevice);
  }

  public switchLamp(switchL: any): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/switch_lamp/`, switchL);
  }

  public setIlluminanceOnLamp(switchL: any): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/brightness_lamp/`, switchL);
  }

  public setAutoLamp(switchL: any): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/auto_lamp/`, switchL);
  }
}
