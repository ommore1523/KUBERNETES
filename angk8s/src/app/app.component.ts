import { Component,OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import {environment as env} from '../environments/environment'
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angk8s';
  host_info:any = {}
  record:any="";
  // hosts_flag:any = true
  all_db_records:any = []
  

  constructor(private http:HttpClient){

  }

  ngOnInit(){

     this.http.get(env.rest_url + '/home',{}).subscribe((data:any)=>{
      this.all_db_records = data['message']['data']
      this.host_info = data['message']['hosts']
    },
    error =>{
      this.host_info = {"flask_host":"NOTFOUND", "flask_ip":"NOTFOUND", "db_host":"NOTFOUND", "db_ip":"NOTFOUND"} 
      this.all_db_records = []
      alert("Backend Stopped Or Backend Error \n" + error.message)
    }
    )

  }



  onAdd(){

    if (this.record != ""){
      console.log("On Add function called ", this.record)
      let params = new HttpParams().set('value', this.record)
      this.http.post(env.rest_url + '/add',params).subscribe((data:any)=>{
        this.all_db_records = data['message']['data']
         this.host_info = data['message']['hosts']
      },
      error => {
        this.host_info = {"flask_host":"NOTFOUND", "flask_ip":"NOTFOUND", "db_host":"NOTFOUND", "db_ip":"NOTFOUND"} 
        this.all_db_records = []
        alert("Backend Stopped Or Backend Error \n" + error.message)
      }
      )
    }
    else{
        alert("Please Add Value")
    }

  }

  onDelete(id:any){

    console.log(id)
    let params = new HttpParams().set('id', id)
    this.http.post(env.rest_url + '/delete',params).subscribe((data:any)=>{
      this.all_db_records = data['message']['data']
      this.host_info = data['message']['hosts']
    },
    error => {
      this.host_info = {"flask_host":"NOTFOUND", "flask_ip":"NOTFOUND", "db_host":"NOTFOUND", "db_ip":"NOTFOUND"} 
      this.all_db_records = []
      alert("Backend Stopped Or Backend Error \n" + error.message)
    }
    )

  }
}
