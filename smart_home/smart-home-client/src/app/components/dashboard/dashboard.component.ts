import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services';

@Component({
  selector: 'app-dashboard',
  templateUrl: 'dashboard.component.html',
})
export class Dashboardomponent implements OnInit{
    constructor(private apiService: ApiService){        
    }

    public ngOnInit(): void {
        this.apiService.getDevices().subscribe(v => console.log(v));
    }
}
