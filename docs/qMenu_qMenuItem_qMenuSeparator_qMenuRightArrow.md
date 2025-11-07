## 设置QMenu的Qss样式

### 1. 设置QMenu的Item样式
```qss
QMenu::item {
    color: #FFFFFF;
    ...
}
```

### 2. 设置QMenu的Separator样式
```qss
QMenu::separator {
    height: 1px;
    margin: 6px;
    ...
}
```

### 3. 设置QMenu右子Menu箭头
```qss
QMenu::right-arror {
    image: url(path);
    width: 12px;
    height: 12px;
    padding-right: 6px;
    ...
}
```