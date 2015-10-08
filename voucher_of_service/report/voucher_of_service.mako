## -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
  <style type="text/css">
  ${css}
  @font-face {
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 400;
    src: local('Roboto Regular'), 
         local('Roboto-Regular'), 
         url(http://themes.googleusercontent.com/static/fonts/roboto/v11/2UX7WLTfW3W8TclTUvlFyQ.woff) 
         format('woff');
  }
  thead {
    display: inline-block;
    width: 100%;
    height: 20px;
  }

  tbody {
    height: 200px;
    width: 100%;
    overflow: auto;
  }

  .note{
    font-size:12px;
  }

  .section_page_break{
    page-break-before: always;
  }

  .list_sale_table td {
    font-family: Roboto;
    border-top: thin solid #EEEEEE;
    text-align:left;
    font-size:10px;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
  }
  .list_sale_table th {
    border-top: thin solid #EEEEEE;
    text-align:center;
    font-size:12px;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
  }

  #wrap_1{
    font-family: Roboto;
    font-size:14px;
    width:100%;
    margin: 0 auto;
    padding-top:15px;
  }
  #included_div{
    width:320px;
    float:left;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:30px;
    border: 1px solid #EEEEEE;
    margin-bottom:20px;
  }
  #excluded_div{
    width:320px;
    float:right;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:30px;
    border: 1px solid #EEEEEE;
    margin-bottom:20px;
  }
  </style>
</head>
<body>
  <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    def gender(g):
        if g == 'False':
            return "Not defined"
        return {'m':'Masculino', 'f':'Femenino'}[g]

    def boolean_string(x):
        return x and "Yes" or "No"
    %>
  %for vos in objects:
  <h1>Voucher Of Service</h1>
  <% setLang(user.lang) %>
  <h3>${vos.folio_id.name}</h3>
  <h4>${vos.folio_id.arrival_date} - ${vos.folio_id.departure_date}</h4>
  <h5>Passengers</h5>
  <table class="list_sale_table" width="100%">
    <tr>
      <th width="15%">Name</th>
      <th width="15%">Lastname</th>
      <th width="15%">Passport</th>
      <th width="15%">Gender</th>
      <th width="60%">Notes / Restrictions</th>
    <tr>
    %for p in vos.passenger_ids:
    <tr>
      <td>${p.firstname}</td>
      <td>${p.lastname}</td>
      <td>${p.ced_ruc}</td>
      <td>${p.gender | gender}</td>
      <td>False</td>
    </tr>
    %endfor%
  </table>
  %endfor%
  <h5>Itinerary</h5>
  %for c in vos.overnight_ids:
    <p class="note">Date: ${c.date}<br />Overnight: ${c.visitpoint_id.name}</p>
    <table class="list_sale_table" width="100%">
      <tr>
        <th>AM / PM</th>
        <th>Location Name</th>
        <th>Visit Point</th>
        <th>Breakfast</th>
        <th>Lunch</th>
        <th>Dinner</th>
        <th>Note</th>
      </tr>
      %for v in c.visitpoint_ids:
      <tr>
        <td>${v.hour}</td>
        <td>${v.location_id.name}</td>
        <td>${v.visitpoint_id.name}</td>
        <td>${v.breakfast | boolean_string}</td>
        <td>${v.lunch  | boolean_string}</td>
        <td>${v.dinner | boolean_string}</td>
        <td>${v.note}</td>
      </tr>
      %endfor
    </table>
  %endfor%
    <section class="section_page_break">
      <div id="wrap_1">
        <div id="included_div" > 
        <h3>Includes</h3>
          <div id="includes_text">${vos.included}</div>
        </div>
        <div id="excluded_div" >
          <h3>Excludes</h3>
          <div id="excluded_text">${vos.excluded}</div>
        </div>
      </div>
    </section>
    <h5>Important notes</h5>
    <p class="note">${vos.important_notes | carriage_returns}</p>
    <section id="contacts" class="note">
      <p>In case of emergency please contact the following phones:</p>
      <div>${vos.emergency_phones | carriage_returns}</div>
      <p>Hotel contact:</p>
      <div>${vos.hotel_contact | carriage_returns}</div>
    </section>
</body>
</html>
