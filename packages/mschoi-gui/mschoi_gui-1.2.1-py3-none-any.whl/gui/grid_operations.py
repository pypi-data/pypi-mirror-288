import wx

# 그리드에 내용 출력하는 반복문 (리스트 형태 버젼)
def grid_print_by_list ( grid, data_list ):
    '''
    리스트 형태의 데이터를 그리드에 넣어주기
    '''
    rownum = grid.GetNumberRows()
    if rownum != 0:
        grid.DeleteRows(pos = 0, numRows = rownum)
    grid.AppendRows(numRows = len( data_list )  )

    for r in range(len( data_list )):
        row_1 = data_list[r]
        for c in range(len(row_1)):
            grid.SetCellValue(int(r), int(c), str(row_1[c]))


# 그리드에 내용 출력하는 반복문 ( 데이터 프레임 버젼 )
def grid_print_by_dataframe( grid, df):
    '''
    데이터 프레임을 그리드에 넣어주기
    '''
    rownum = grid.GetNumberRows()
    if rownum != 0:
        grid.DeleteRows(pos = 0, numRows = rownum)
    grid.AppendRows(numRows = df.shape[0]  )
    for r in range(len( df )):
        for c in range(df.shape[1]):
            grid.SetCellValue(int(r), int(c), str(df.iloc[r,c]))


# 그리드 내용을 초기화 해주기
def clear_grid_row(grid):
    '''
    그리드 로우 초기화(로우 전체 제거)
    '''
    rownum = grid.GetNumberRows()
    grid.DeleteRows(pos = 0, numRows = rownum)
    grid.AppendRows(numRows = 100)


########################################################################
# 컬럼 헤더부분 클릭시 해당 컬럼 기준으로 그리드 정렬
# 프레임 생성자에 self.sorted = True 선언 해두고 프레임마다 아래 처럼 써야함 (토글처럼 작동시키기임)
# function.sort_by_column(grid, col, self.sorted)  
# self.sorted = not self.sorted
########################################################################
def sort_by_column( grid, col_no, ascending:bool ):
    '''
    컬럼 클릭시 오름, 내림차순을 토글링으로 정렬해주는 함수
    '''
    grid_data = []
    for row in range(grid.GetNumberRows()):
        row_data = []
        for col in range(grid.GetNumberCols()):
            cell_value = grid.GetCellValue(row, col)
            row_data.append(cell_value)
        grid_data.append(row_data)
    
    grid_data.sort(key=lambda x: x[col_no], reverse=not ascending)
    grid.ClearGrid()

    for i, row_data in enumerate(grid_data):
        for j, cell_value in enumerate(row_data):
            grid.SetCellValue(i, j, cell_value)


def sort_by_column_end_row(grid, col_no, ascending:bool, start_row=0, end_row=None):
    '''
    컬럼 클릭시 정해진 로우(end_row)까지만 정렬 해주는 함수
    '''
    if end_row is None or end_row > grid.GetNumberRows():
        end_row = grid.GetNumberRows()

    grid_data = []
    # 전체 그리드 데이터를 저장 (정렬 범위 외 데이터 포함)
    for row in range(grid.GetNumberRows()):
        row_data = []
        for col in range(grid.GetNumberCols()):
            cell_value = grid.GetCellValue(row, col)
            row_data.append(cell_value)
        grid_data.append(row_data)

    # 지정된 범위 내의 로우만 정렬
    grid_data[start_row:end_row] = sorted(grid_data[start_row:end_row],
                                          key=lambda x: x[col_no],
                                          reverse=not ascending)
    grid.ClearGrid()

    # 정렬된 데이터를 그리드에 다시 설정
    for i, row_data in enumerate(grid_data):
        for j, cell_value in enumerate(row_data):
            grid.SetCellValue(i, j, cell_value)


def set_column_alignment(grid, col, alignment):
    '''
    컬럼 정렬해주기(오른쪽, 왼쪽, 가운데 정렬)
    ex) set_column_alignment(grid, 3, wx.ALIGN_LEFT)
    '''
    attr = wx.grid.GridCellAttr()
    attr.SetAlignment(alignment, wx.ALIGN_CENTER)  # Vertical alignment is centered
    grid.SetColAttr(col, attr)
        



# 그리드에서 선택된 셀의 값을 반환
def get_selected_cellvalue( grid, key_col_no ):
    '''
    그리드에서 블럭으로 설정된 범위의 값들을 반환
    '''
    # 그리드에서 선택된 셀의 값을 반환 
    # 1. 여러 컬럼이 선택된 경우 오류
    # 2. 선택된 블럭에서의 로우 범위를 구함
    # 3. 해당 로우 범위에서 원하는 컬럼의 데이터 (키 리스트)를 구해서 리턴
    # 4. 리턴값 : 키 리스트, edit 컬럼 번호
    
    topLeftCells = grid.GetSelectionBlockTopLeft()
    bottomRightCells = grid.GetSelectionBlockBottomRight()


    top_col_no = [coord[1] for coord in topLeftCells]
    bottom_col_no = [coord[1] for coord in bottomRightCells]

    if top_col_no != bottom_col_no or top_col_no == []:
        return None, None
    
    top_row_no = [coord[0] for coord in topLeftCells]
    bottom_row_no = [coord[0] for coord in bottomRightCells]

    key_list = {}

    for i in range(int(top_row_no[0]), int(bottom_row_no[0]) + 1):
        key_list[grid.GetCellValue(i, key_col_no)] = grid.GetCellValue(i, top_col_no[0])

    return key_list, top_col_no[0]
