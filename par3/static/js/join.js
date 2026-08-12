document.addEventListener('DOMContentLoaded', function () {

  const tableBody = document.getElementById('j_table_body');
  const tabAll = document.getElementById('j_tab_all');
  const tabDate = document.getElementById('j_tab_date');
  const tabPrice = document.getElementById('j_tab_price');
  const tabUrgent = document.getElementById('j_tab_urgent');
  const selectedTagsRow = document.getElementById('j_selected_tags_row');
  const selectedTagsWrap = document.getElementById('j_selected_tags');
  const excludeFullCheckbox = document.getElementById('j_exclude_full_checkbox');
  const searchInput = document.querySelector('.j_filter_search');
  const resetBt = document.getElementById('j_reset_bt');

  const myFilterBt = document.getElementById('j_my_filter_bt');
  const myFilterBtText = document.getElementById('j_my_filter_bt_text');
  const myFilterEl = document.getElementById('j_my_filter');
  let myFilterValue = 'all';

  const originalRows = Array.from(tableBody.querySelectorAll('.jt_row'));

  let currentSort = 'all';
  const selectedFilters = { region: [], condition: [], time: [] };

  // ------------------------------------------------
  // 하트(좋아요) 클릭 - 서버 API 연동
  // ------------------------------------------------
  originalRows.forEach(function (row) {
    const heart = row.querySelector('.jt_heart_bt');
    const joinId = row.dataset.joinId;

    heart.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      fetch('/join/api/toggle_like/' + joinId, {
        method: 'POST',
      })
        .then(function (res) {
          if (res.status === 401) {
            window.location.href = '/auth/login?next=' + encodeURIComponent(window.location.pathname);
            return null;
          }
          return res.json();
        })
        .then(function (data) {
          if (data) {
            row.dataset.liked = data.liked ? 'true' : 'false';
          }
        });
    });
  });

  // ------------------------------------------------
  // 지역/조건/시간대 드롭다운
  // ------------------------------------------------
  document.querySelectorAll('.j_dropdown').forEach(function (dropdown) {
    const btn = dropdown.querySelector('.j_dropdown_bt');

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      const isOpen = dropdown.classList.contains('j_dropdown--open');

      document.querySelectorAll('.j_dropdown').forEach(function (d) {
        d.classList.remove('j_dropdown--open');
      });
      if (!isOpen) dropdown.classList.add('j_dropdown--open');
    });
  });

  document.addEventListener('click', function () {
    document.querySelectorAll('.j_dropdown').forEach(function (d) {
      d.classList.remove('j_dropdown--open');
    });
    if (myFilterEl) {
      myFilterEl.classList.remove('j_my_filter--open');
    }
  });

  function bindDropdownCheckboxes(dropdownId, filterKey) {
    const dropdown = document.getElementById(dropdownId);
    const checkboxes = dropdown.querySelectorAll('.j_dropdown_option input[type="checkbox"]');

    checkboxes.forEach(function (checkbox) {
      checkbox.addEventListener('change', function () {
        if (checkbox.checked) {
          selectedFilters[filterKey].push(checkbox.value);
        } else {
          selectedFilters[filterKey] = selectedFilters[filterKey].filter(function (v) {
            return v !== checkbox.value;
          });
        }
        renderTags();
        applyFilterAndSort();
      });
    });
  }

  bindDropdownCheckboxes('j_dropdown_region', 'region');
  bindDropdownCheckboxes('j_dropdown_condition', 'condition');
  bindDropdownCheckboxes('j_dropdown_time', 'time');

  function hasAnyFilterSelected() {
    return selectedFilters.region.length > 0
        || selectedFilters.condition.length > 0
        || selectedFilters.time.length > 0;
  }

  function renderTags() {
    selectedTagsWrap.innerHTML = '';

    Object.keys(selectedFilters).forEach(function (filterKey) {
      selectedFilters[filterKey].forEach(function (value) {
        const tag = document.createElement('span');
        tag.className = 'j_tag';
        tag.innerHTML = value + ' <span class="j_tag_remove" data-key="' + filterKey + '" data-value="' + value + '">×</span>';
        selectedTagsWrap.appendChild(tag);
      });
    });

    selectedTagsWrap.querySelectorAll('.j_tag_remove').forEach(function (removeBtn) {
      removeBtn.addEventListener('click', function () {
        const key = removeBtn.dataset.key;
        const value = removeBtn.dataset.value;

        selectedFilters[key] = selectedFilters[key].filter(function (v) {
          return v !== value;
        });

        document.querySelectorAll('.j_dropdown_option input[value="' + value + '"]').forEach(function (cb) {
          cb.checked = false;
        });

        renderTags();
        applyFilterAndSort();
      });
    });

    if (hasAnyFilterSelected()) {
      selectedTagsRow.classList.add('j_selected_tags_row--visible');
    } else {
      selectedTagsRow.classList.remove('j_selected_tags_row--visible');
    }
  }

  resetBt.addEventListener('click', function () {
    selectedFilters.region = [];
    selectedFilters.condition = [];
    selectedFilters.time = [];

    document.querySelectorAll('.j_dropdown_option input[type="checkbox"]').forEach(function (cb) {
      cb.checked = false;
    });

    renderTags();
    applyFilterAndSort();
  });

  excludeFullCheckbox.addEventListener('change', applyFilterAndSort);

  searchInput.addEventListener('input', applyFilterAndSort);

  // ------------------------------------------------
  // 참여중/내모집/관심글/참여가능 드롭다운
  // ------------------------------------------------
  if (myFilterBt) {
    myFilterBt.addEventListener('click', function (e) {
      e.stopPropagation();
      myFilterEl.classList.toggle('j_my_filter--open');
    });

    document.querySelectorAll('input[name="my_filter"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        myFilterValue = radio.value;
        myFilterBtText.textContent = radio.parentElement.textContent.trim();
        myFilterEl.classList.remove('j_my_filter--open');
        applyFilterAndSort();
      });
    });
  }

  // ------------------------------------------------
  // 필터 + 정렬 적용 (핵심 함수)
  // ------------------------------------------------
  function applyFilterAndSort() {
  const keyword = searchInput.value.trim().toLowerCase();

  let rows = originalRows.filter(function (row) {
    if (selectedFilters.region.length > 0 && !selectedFilters.region.includes(row.dataset.region)) {
      return false;
    }
    if (selectedFilters.condition.length > 0 && !selectedFilters.condition.includes(row.dataset.condition)) {
      return false;
    }
    if (selectedFilters.time.length > 0 && !selectedFilters.time.includes(row.dataset.timeslot)) {
      return false;
    }
    if (excludeFullCheckbox.checked && Number(row.dataset.filled) >= Number(row.dataset.total)) {
      return false;
    }

    if (myFilterValue === 'applied' && (row.dataset.isApplied !== 'true' || row.dataset.isOwner === 'true')) {
      return false;
    }
    if (myFilterValue === 'owner' && row.dataset.isOwner !== 'true') {
      return false;
    }
    if (myFilterValue === 'liked' && row.dataset.liked !== 'true') {
      return false;
    }
    if (myFilterValue === 'available' && (row.dataset.isFull === 'true' || row.dataset.isApplied === 'true' || row.dataset.isOwner === 'true')) {
      return false;
    }

    if (keyword && !row.dataset.keyword.toLowerCase().includes(keyword)) {
      return false;
    }
    return true;
  });

  rows = sortRows(rows, currentSort);
  renderRows(rows);
}

  function sortRows(rows, sortType) {
    const copied = rows.slice();

    if (sortType === 'date') {
      copied.sort(function (a, b) {
        return a.dataset.date.localeCompare(b.dataset.date);
      });
    } else if (sortType === 'price') {
      const order = tabPrice.dataset.order;
      copied.sort(function (a, b) {
        const priceA = Number(a.dataset.price);
        const priceB = Number(b.dataset.price);
        return order === 'asc' ? priceA - priceB : priceB - priceA;
      });
    } else if (sortType === 'urgent') {
      copied.sort(function (a, b) {
        const ratioA = Number(a.dataset.filled) / Number(a.dataset.total);
        const ratioB = Number(b.dataset.filled) / Number(b.dataset.total);
        if (ratioB !== ratioA) return ratioB - ratioA;
        return a.dataset.date.localeCompare(b.dataset.date);
      });
    }

    return copied;
  }

  function renderRows(rows) {
    tableBody.innerHTML = '';
    rows.forEach(function (row) {
      tableBody.appendChild(row);
    });
  }

  function setActiveTab(clickedTab) {
    document.querySelectorAll('.j_tab').forEach(function (tab) {
      tab.classList.remove('j_tab--active');
    });
    clickedTab.classList.add('j_tab--active');
  }

  tabAll.addEventListener('click', function () {
    setActiveTab(tabAll);
    currentSort = 'all';
    applyFilterAndSort();
  });

  tabDate.addEventListener('click', function () {
    setActiveTab(tabDate);
    currentSort = 'date';
    applyFilterAndSort();
  });

  tabPrice.addEventListener('click', function () {
    setActiveTab(tabPrice);
    currentSort = 'price';
    applyFilterAndSort();
    tabPrice.dataset.order = tabPrice.dataset.order === 'asc' ? 'desc' : 'asc';
  });

  tabUrgent.addEventListener('click', function () {
    setActiveTab(tabUrgent);
    currentSort = 'urgent';
    applyFilterAndSort();
  });

});