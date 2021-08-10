import { HttpClient } from '@angular/common/http';
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

  public getDevices(): Observable<DeviceDto[]> {
    return this.http.get<any>(`${this.apiUrl}/devicedevice/`);
  }

  public getDevice(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/devicedevice/${id}/`);
  }
  public registerDevices(newDevice: DeviceDto): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/register_device/`, newDevice);
  }
  public updateDevices(newDevice: { id: string }): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/update_device/`, newDevice);
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
