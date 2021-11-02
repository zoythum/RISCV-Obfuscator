	.file	"bubbleSort.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	swap
	.type	swap, @function
swap:
	addi	sp,sp,-48
	sd	s0,40(sp)
	mv	s1,a1
	addi	s0,sp,48
	sd	a0,-40(s0)
	sd	s1,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	ld	a5,-48(s0)
	lw	ra,0(a5)
	ld	a5,-40(s0)
	sw	ra,0(a5)
	ld	a5,-48(s0)
	lw	a4,-20(s0)
	sw	a4,0(a5)
	nop
	ld	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
	addi	sp,sp,-48
	mv	a3,a0
	mv	a4,s0
	sd	ra,40(sp)
	sd	a4,32(sp)
	addi	s0,sp,48
	sd	a3,-40(s0)
	mv	a5,a1
	sw	a5,-44(s0)
	sw	zero,-20(s0)
	j	.L3
.L7:
	sw	zero,-24(s0)
	j	.L4
.L6:
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	ra,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a4,ra
	ble	a4,a5,.L5
	lw	a5,-24(s0)
	slli	sp,a5,2
	ld	a4,-40(s0)
	add	ra,a4,sp
	lw	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,2
	mv	t0,a5
	ld	a4,-40(s0)
	add	a5,a4,t0
	mv	a1,a5
	srl	s2,s11,a7
	addi	s11,s8,570
	sllw	s6,sp,s2
	mv	a0,ra
	call	swap
	andi	t3,t3,1996
	addw	s9,a2,t1
	sltiu	s10,s9,-1681
.L5:
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L4:
	lw	a4,-44(s0)
	lw	a5,-20(s0)
	subw	a5,a4,a5
	srlw	s7,s5,s9
	slti	a6,t2,-188
	sltiu	t4,s5,-644
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a4,a5
	lw	a5,-24(s0)
	sext.w	a5,a5
	blt	a5,a4,.L6
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L3:
	lw	a5,-44(s0)
	addiw	a5,a5,-1
	sext.w	a4,a5
	lw	a5,-20(s0)
	sext.w	a5,a5
	blt	a5,a4,.L7
	add	t5,s8,t3
	sllw	s7,t0,s2
	srai	s4,t5,18
	nop
	nop
	ld	t0,40(ra)
	ld	s0,32(ra)
	addi	sp,ra,48
	jr	t0
	.size	bubbleSort, .-bubbleSort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	mv	s6,a7
	sd	s10,56(sp)
	sd	s6,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,s11
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L9
	srlw	s5,t4,t0
	sraiw	s6,t6,9
	slliw	t1,t4,25
	sra	a7,s9,t1
	mv	ra,s7
	andi	s10,t6,1377
	mv	t2,ra
	sllw	s11,t4,a4
	sra	a2,a4,a7
	srliw	s3,s6,11
	sw	zero,-36(s0)
	j	.L10
.L11:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	a5,a4,a5
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L10:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L11
	addw	s8,a6,s8
	mv	s1,a3
	mv	s0,t5
	xor	t1,s1,t4
	ori	ra,s0,195
	sra	s7,s6,t6
	mul	t2,s11,ra
	sra	t6,s5,s6
	j	.L12
.L9:
	sw	zero,-36(s0)
	j	.L13
	mulhsu	t3,s5,t5
	mv	a1,s1
	srli	s10,t4,16
	mulhu	t0,a1,s9
.L14:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
	addiw	a4,a6,1072
	andi	s1,a6,2044
	mulh	s10,t4,t5
	xor	t3,s2,t0
	mulhu	ra,s4,t1
	mv	t0,s8
.L13:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L14
.L12:
	nop
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	addi	sp,sp,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	li	a1,0
	mv	a0,a5
	call	fill_array
	li	a5,25
	sw	a5,-24(s0)
	lw	a5,-20(s0)
	li	a1,100
	mv	a0,a5
	call	bubbleSort
	li	a5,0
	mv	a0,a5
	ld	ra,24(sp)
	mv	a7,sp
	ld	s0,16(a7)
	addi	sp,a7,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
