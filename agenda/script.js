function renderDate(data, type, row) {
  let date = new Date(data);
  if (type === "display") {
      if (!date) {
          return unknownText;
      }
      return date.toLocaleDateString('de-CH', { weekday: "long", day: "2-digit", month: "2-digit", year: "numeric" });
  }
  if (date) {
      return date.getTime();
  }
  return Number.MAX_VALUE;
}

function renderTime(data, type, row) {
  let date = new Date(data);
  if (type === "display") {
      if (!date || (date.getHours() === 0 && date.getMinutes() === 0)) {
          // No time or time is midnight
          return unknownText;
      }
      return date.toLocaleTimeString('de-CH', { hour: "2-digit", minute: "2-digit" });
  }
  if (date) {
      return date.getTime();
  }
  return Number.MAX_VALUE;
}

function renderLocation(data, type, row) {
  let location = row.location.displayName;
  try {
      if (row.location.address.street !== undefined) {
          location += '<br />' + row.location.address.street + 
              '<br />' + row.location.address.postalCode + ' ' + row.location.address.city +
              '<br />[' + row.location.coordinates.latitude + ' | ' + row.location.coordinates.longitude + ']';
          }
  } catch (error) {
      
  }
  return location;
}

class PopUp {
  constructor() {
      this._subject = document.getElementById("datatableModalTitle");
      this._description = document.getElementById("datatableModalBody");
  }

  set modalwindow(details) {
      this._subject.innerHTML = "BodyContent";
      this._description.innerHTML = details.body.content;
      if (this._description.innerHTML !== '') {
          this._description.innerHTML += 
              `<hr />
              <ul tal:condition="python:this.attr('dataurl')=='unibeagenda@engineerer.ch'">
              <li><a href="#" target="_blank"
                  tal:define="attachment_id python:'AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAAMK4KtAAAARIAEABSfkuR30dnQbt9Abbr3geI'"
                  tal:attributes="href python:'getAgendaAttachment?id='+attachment_id"
                  tal:content="python:OutlookConnector.run_asyncio(outlook.get_calendar_attachments(attachment_id))">foo.pdf</a></li>
              <li><a href="#" target="_blank"
                  tal:define="attachment_id python:'AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAAMK4KtAAAARIAEAAFFVWgL_vmR4sCmD7sgO0a'"
                  tal:attributes="href python:'getAgendaAttachment?id='+attachment_id"
                  tal:content="python:OutlookConnector.run_asyncio(outlook.get_calendar_attachments(attachment_id))">bar.pdf</a></li>
              </ul>`;
      }
  }
}

$(document).ready(() => {
  
  let popup = new PopUp();
  
  // Replace with actual popup function.
  let assignClickListener = (row, bodycontent) => {
      row.addEventListener("click", () => {
          popup.modalwindow = bodycontent;
          $('#datatableModal').modal('toggle');
      });
  };
  
  $("#table").DataTable({
      processing: true,
      ajax: {
          url: 'http://localhost:63342/unibe-cms/frontend/zms/datatables/agenda/2025-04-06T11_05_35+02_00.json', 
          dataSrc: '', // read data from a plain array rather than an array in an object
          dataType: "json"
      },
      columns: [
          {data: "start.dateTime", name: "start.dateTime", render: renderDate},
          {data: "start.dateTime", name: "start.dateTime", render: renderTime},
          {data: "end.dateTime", name: "end.dateTime", render: renderDate},
          {data: "end.dateTime", name: "end.dateTime", render: renderTime},
          {data: "subject", name: "subject"},
          {data: "location", name: "location", render:renderLocation},
          {data: "categories", name: "categories"},
          {data: "bodyPreview", name: "bodyPreview"},
      ],
      autoWidth: false,
      createdRow: assignClickListener,
      order: [[ 0, 'asc' ], [ 1, 'asc' ]],
      ordering: true,
      asStripeClasses: [],        // disable zebra coloring of rows
      pageLength: 25,
  });
});